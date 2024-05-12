# external imports
import abc
import time
from typing import Any, List, Union

from pyqflow.asynchronous import Queue

# internal imports.
from pyqflow.constants import BRANCH, CTRL, DEFAULT_BATCH, MAX_BUFFER_SIZE, SEP, STOP

# moovs imports.
from pyqflow.reader import video_reader
from pathlib import Path
import asyncio
import cv2
import numpy as np


class QActor:
    """Node of the workflow pipeline.

    This entity represents a node in the workflow DAG and allows for async reading and writing to a stream and manages the node's input connections.
    """

    def __init__(
        self,
        name: str,
        source: bool = False,
        buffer_size: int = DEFAULT_BATCH,
        control: bool = False,
    ):
        """Creates an actor stream.

        Args:
            name (str): Identifier of this node.
            source (bool): Whether this node is a source stream.
        """
        self.name = name
        self.parents = []
        self.children = {}

        self.__source = source
        self.__control = control
        self.buffer_size = buffer_size

        self.queue = Queue(maxsize=buffer_size)

    def source(self):
        return self.__source

    def runnable(self):
        return not self.__control

    def control(self):
        return self.__control

    def add_parent(self, parent: "QActor"):
        """Links a source actor to this actor stream, following the provided process.

        Args:
            process (QProcess): process that transforms the parent actor and produces data into this actor stream.
            parent (Qactor): source actor stream.
        """
        self.parents.append(parent)

    def add_child(
        self,
        child: "QActor",
        queue: Queue = None,
        qindex: Union[None, int] = None,
        limitless=False,
    ):
        """Adds a child actor stream to this actor stream.

        Args:
            child (QActor): actor stream to be added as a child.
        """
        if queue is None:
            if not limitless:
                queue = Queue(self.buffer_size)
            else:
                queue = Queue(MAX_BUFFER_SIZE)

        self.children[child] = (queue, qindex)

        #

    async def stop(self):
        """Closes the actor stream

        Sends a STOP marker to the actor stream indicating the consumers that there will be no more data coming.
        """

        if len(self.children) > 0:
            for queue, _ in self.children.values():
                await queue.put(STOP)
            # print(f"Stopping {self}: STOP. ")
        else:
            await self.queue.put(STOP)

    async def commit(self, key: str, value: Any):
        """Adds a key-value pair to the actor stream.

        Args:
            key (Any): identifier.
            value (Any): data.
        """

        if self.__control:
            key = CTRL + key

        if len(self.children) > 0:
            for queue, qid in self.children.values():
                if qid is None:
                    await queue.put((key, value))
                else:
                    await queue.put((f"{qid}{BRANCH}{key}", value))
        else:
            await self.queue.put((key, value))

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    async def tolist(self) -> List[Any]:
        """Consumes the actor stream and appends everything to a list.

        Returns:
            List[Any] : A list of element of the actor stream.
        """

        results = []

        async for id, data in self.iterable():
            results.append((id, data))

        return results

    async def iterable(self, node: Union["QActor", None] = None):
        """Produces an async iterable for consuming the actor stream.

        Yields:
            key, value : actor stream's key value pairs.
        """
        loop = True

        if node is None:
            queue = self.queue
        else:
            assert (
                node in self.children
            ), f"The actor {node} is not linked to this actor {self}."
            queue, _ = self.children[node]

        while loop:
            value = await queue.get()

            if value == STOP:
                loop = False
            else:
                yield value


class QControl(QActor):
    def __init__(self, name: str, **kwargs):
        super().__init__(name=name, **kwargs)

        self.control = QActor(name=f"{name}{SEP}ctrl", source=False, control=True)


class QSource(QActor):
    """Input Node of the workflow pipeline.

    This entity represents the data entrypoint of the workflow DAG.
    """

    def __init__(self, name: str, **kwargs):
        """Creates a source actor stream.

        Args:
            name (str): Identifier of this source node.
        """
        super().__init__("Source:" + name, source=True, **kwargs)

    @abc.abstractmethod
    async def feed(self):
        """This method should starting producing data to the actor stream from io."""
        raise NotImplementedError()


class QIterable(QSource):
    """Input node for the workflow pipeline from a iterable source.

    Given an iterable creates a source actor.
    """

    def __init__(self, name, iterable, keyvalue: bool = True, **kwargs):
        """Creates a source actor based on a given iterable.

        Args:
            iterable (iterable): data to feed to this actor stream.
            keyvalue (bool): if the iterable is a key-value pair.
        """
        super().__init__(name=name, **kwargs)
        self.python_iterable = iterable

        if keyvalue:
            self.feed = self.__feed_kv
        else:
            self.feed = self.__feed

    def append(self, value):
        self.python_iterable.append(value)

    async def __feed_kv(self):
        """Produces key value pairs to the stream based on the saved itearable."""
        count = 0
        for key, item in self.python_iterable:
            await self.commit(str(key), item)

            count += 1

        await self.stop()

    async def __feed(self):
        """Produces datapoints to the stream base on the saved iterable."""
        count = 0
        for item in self.python_iterable:
            await self.commit(str(count), item)
            count += 1

        await self.stop()


class QVideo(QSource):
    """Creates a source actor based a video file.

    Reads in async way using ffmpeg a video file and adds it to the audio stream.
    """

    def __init__(
        self,
        video_path: str,
        rgb: bool = False,
        resolution: Union[None, int] = None,
        batch: int = 32,
        buffer_size: int = 5,
        persistent: bool = False,
        frames: int = 900,
        fps: int = 30,
    ):
        """Initiates the video source actor.

        Args:
            video_path (str): source video path.
            fps (int): number of frames to read per second. Defaults to 32.
            rgb (bool): If yes uses rgb else bgr. Defaults to False.
            resolution (int, None): output video resolution. Defaults to None.
            batch (int): Number of frames composing a batch. Defaults to 32.
            buffer_size (int): number prefetched batches. Defaults to 8.
            persistent (bool): Save to ray's memcache or not. Defaults to True.

        Initiates de ffmpeg reading process and queue and creates an async iterable reading from the queue.
        """

        # Ensure the video actually exists
        if not Path(video_path).exists():
            raise FileNotFoundError(f"Video at path {video_path} does not exist.")

        self.video_path = video_path
        self.rgb = rgb
        self.resolution = resolution
        self.batch = batch
        self.buffer_size = buffer_size
        self.persistent = persistent
        self.frames = frames
        self.fps = fps

        super().__init__("Video")

    async def feed(self):
        i = 0
        """Produces datapoints to the stream base on the saved iterable."""
        async for key, item in self.video_feed():
            await self.commit(str(key), item)
            i += 1

            # if i > 20:
            #     break

        await self.stop()

    async def video_feed(self):
        async for key, item in video_reader(
            source=self.video_path,
            fps=self.fps,
            rgb=self.rgb,
            resolution=self.resolution,
            batch=self.batch,
            buffer_size=self.buffer_size,
            label=True,
            persistent=self.persistent,
            frames=self.frames,
        ):
            yield key, item


class QFileSource(QSource):
    """Input node for the workflow pipeline from a file source."""

    def __init__(self, file_path, **kwargs):
        """Creates a source actor based on a given file.

        Args:
            file_path (str): data to feed to this actor stream.
        """
        super().__init__(name="file-source-" + file_path, **kwargs)
        self.file_path = file_path

        # self.feed = self.__feed

    async def feed(self):
        """Produces datapoints to the stream base on the saved iterable."""

        count = 0

        with open(self.file_path, "r") as f:
            lines = f.readlines()

        for key, item in enumerate(lines):
            await self.commit(str(key), item)

        await self.stop()


class QImage(QSource):
    def __init__(self, image_path: Union[str, Path], **kwargs):
        super().__init__(name="image-" + image_path, **kwargs)
        self.image_path = image_path

        # Ensure the existance of said image
        if not Path(self.image_path).exists():
            raise FileNotFoundError(f"Image at path {self.image_path} does not exist.")

    async def feed(self):
        img = await self._loadimage()
        await self.commit(str(self.image_path), img)
        await self.stop()

    async def _loadimage(self):
        loop = asyncio.get_running_loop()

        def wrapped_cv2_read(x: str):
            im = cv2.imread(x)

            # Add batch dimension
            return im[None]

        try:
            img = await loop.run_in_executor(None, wrapped_cv2_read, self.image_path)
            return img
        except Exception as err:
            print(
                f"Error loading image at path {self.image_path} with exception: {err}"
            )

    def get(self) -> np.ndarray:
        return cv2.imread(self.image_path)
