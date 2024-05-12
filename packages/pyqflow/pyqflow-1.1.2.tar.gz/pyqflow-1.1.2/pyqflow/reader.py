# Standard Libraries
import asyncio
import os
from asyncio import Queue

import cv2
import ffmpeg
import numpy as np

# qflow
from pyqflow.exceptions import VideoTooSmallException

STOP = None


def get_video_frame_count(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file was opened successfully
    if not cap.isOpened():
        raise Exception("Could not open video file - Video to small")
        # return -1  # Return -1 if the video file could not be opened
    # use 30 fps
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Get the total number of frames in the video
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # Release the video file
    cap.release()
    # return frame count
    return frame_count


def query_resolution(source_path):
    vid = cv2.VideoCapture(source_path)
    height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    vid.release()
    if width == 0 or height == 0:
        raise VideoTooSmallException()
    return int(width), int(height)


def articulate_resolution(source_shape, target_resolution: int = 720):
    if len(source_shape) > 2:
        source_shape = source_shape[:2]

    source_shape = np.array(source_shape)
    i = np.argmin(source_shape)
    cov_i = 1 - i

    vi = source_shape[i]

    scale_factor = target_resolution / vi
    source_shape[i] = target_resolution
    source_shape[cov_i] = int(scale_factor * source_shape[cov_i])

    return source_shape.tolist()


async def __batch_video_reader(
    source,
    queue,
    fps=30,
    rgb=False,
    resolution=None,
    batch=1,
    func=lambda x: x,
    threads=4,
    timelimit=30,
):
    if not os.path.exists(source):
        await queue.put(STOP)
        raise Exception(f"Video does not exist at {source}")

    pix_fmt = "rgb24" if rgb else "bgr24"
    try:
        width, height = query_resolution(source_path=source)
    except Exception as e:
        await queue.put(STOP)
        raise Exception(f"Video has no content at {source}")

    process = ffmpeg.input(source)
    ffmpeg_args = {
        "format": "image2pipe",
        "pix_fmt": pix_fmt,
        "r": str(fps),
        "t": timelimit,
        "threads": threads,
        "vcodec": "rawvideo",
    }
    try:
        if not (resolution is None):
            dim = articulate_resolution((width, height), resolution)
            height, width = dim
            shape = (width, height, 3)
            ffmpeg_args["s"] = f"{height}x{width}"
        else:
            shape = (height, width, 3)
            ffmpeg_args["s"] = f"{width}x{height}"

    except Exception as e:
        await queue.put(STOP)
        return e

    process = process.output("pipe:", **ffmpeg_args)
    process = process.run_async(pipe_stdout=True, quiet=True)

    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await asyncio.create_task(
        asyncio.get_running_loop().connect_read_pipe(lambda: protocol, process.stdout)
    )

    i = 0
    try:
        while True:
            try:
                in_bytes = await reader.readexactly(batch * width * height * 3)
            except asyncio.IncompleteReadError as e:
                break

            in_frame = np.frombuffer(in_bytes, np.uint8).reshape([batch, *shape])
            # print(f"Reading batch {batch} in timestamp {i}")
            await queue.put(func(in_frame))

            i += 1
            if len(in_bytes) < batch * width * height * 3:
                break

    finally:
        await queue.put(STOP)
        process.stdout.close()
        process.wait()


async def video_reader(
    source,
    fps=30,
    rgb=False,
    resolution=None,
    batch=1,
    func=lambda x: x,
    buffer_size=10,
    label=False,
    persistent=False,
    frames=900,
    threads=4,
):
    limit = np.ceil(frames / batch)
    timelimit = np.ceil(frames / fps)
    q = Queue(maxsize=buffer_size)

    error_msg_packed = asyncio.create_task(
        __batch_video_reader(
            source=source,
            queue=q,
            fps=fps,
            rgb=rgb,
            resolution=resolution,
            batch=batch,
            func=func,
            threads=threads,
            timelimit=timelimit,
        )
    )

    i = 0
    count = 0
    while True:
        b = await q.get()

        if b is STOP:
            break

        if i < limit:
            if count + b.shape[0] > frames:
                b = b[: frames - count]
            count += b.shape[0]

            if persistent:
                b_ref = b.copy()
            else:
                b_ref = b

            if label:
                yield i, b_ref
            else:
                yield b_ref

        i += 1

    error_msg = await error_msg_packed

    if isinstance(error_msg, Exception):
        raise error_msg
