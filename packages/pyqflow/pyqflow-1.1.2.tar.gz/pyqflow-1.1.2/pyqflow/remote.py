import logging
import asyncio
import random
from typing import Any

import aiohttp
from aiohttp import ClientSession
from aiohttp.client_exceptions import ServerDisconnectedError
import logging

HttpSession = ClientSession


trace_config = aiohttp.TraceConfig()


async def post(
    url: str,
    data: bytes,
    session: HttpSession,
    maximum_backoff: int = 10,
    max_retries: int = 50,
    minimum_retries: int = 5,
    **kwargs,
) -> Any:
    """Sends a POST request to `url` with `data` and awaits result.
    This function implements an exponential backoff algorithm that retries requests exponentially,
    increasing the waiting time between retries up to a maximum backoff time. For example:

    Make a request to Quokka.

     - If the request fails, wait 1 + random_number_milliseconds seconds and retry the request.
     - If the request fails, wait 2 + random_number_milliseconds seconds and retry the request.
     - If the request fails, wait 4 + random_number_milliseconds seconds and retry the request.

    And so on, up to a maximum_backoff time.

    Continue waiting and retrying up to some maximum number of retries.

    where:
    The wait time is min(((2^n)+random_number_milliseconds), maximum_backoff), with n incremented by 1 for each iteration (request).
    maximum_backoff is will be 1 minute (60 seconds). The appropriate value depends on the use case.

    Args:
        url (str): http resource url.
        data (bytes): serialized data to be sent.
        session (HttpSession): Http session.
        maximum_backoff: maximum backoff time
        max_retires: maximum number of retires. in 6 iteration it will reach 64 seconds, so use 7 iterations

    Returns:
        Any: remote service response.
    """
    iteration = 0
    outputs = None
    while iteration < max_retries:
        is_server_disconnected = False

        try:
            resp = await session.post(url=url, data=data, **kwargs)
        except:
            is_server_disconnected = True

        if is_server_disconnected or resp.status != 200:
            if not is_server_disconnected:
                content = await resp.text()
                logging.error(
                    f"Failed to connect to the remote service. Status: {resp.status}. Content: {content}"
                )

            iteration += 1

            if iteration <= minimum_retries:
                wait_time = 0
            else:
                # random_number_milliseconds is a random number of milliseconds less than or equal to 1000. This helps to avoid cases in which many clients are synchronized by some situation and all retry at once, sending requests in synchronized waves. The value of random_number_milliseconds is recalculated after each retry request.
                random_number_milliseconds = random.random()
                wait_time = min(
                    ((1.5**iteration) + random_number_milliseconds), maximum_backoff
                )
                await asyncio.sleep(wait_time)

            continue

        outputs = await resp.json()
        break

    if outputs is None:
        raise Exception("Failed to connect to the remote service.")

    return outputs["outputs"]


def request_broadcast(url: str, pack_function, unpack_function, **kwargs):
    """Creates a request function.

    Args:
        url (str): http resource url.
        pack_function (function): function to serialize data.
        unpack_function (function): function to integrate the response.
    """
    org_kwargs = kwargs

    async def piperequest(data: Any, session: HttpSession):
        """Sends a POST request to `url` with `data` and awaits result in the provided session.

        Args:
            data (Any): data to be sent.
            session (HttpSession): Ongoing Http session.

        Returns:
            Any : reponse from remote service.
        """
        try:
            data_o = pack_function(data)
            kwargs = None

            if isinstance(data_o, list) or isinstance(data_o, tuple):
                kwargs = data_o[1:]
                data_o = data_o[0]

            # data must be serialized in bytes or json
            result = await post(url=url, data=data_o, session=session, **org_kwargs)

            # return result from the unpack function
            result = unpack_function(data, result, kwargs)
        except Exception as e:
            logging.exception(f"Failed to connect to the remote service. ERROR: {e}")

        return result

    return piperequest
