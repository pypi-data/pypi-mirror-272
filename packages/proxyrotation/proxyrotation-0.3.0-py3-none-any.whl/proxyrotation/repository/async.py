import asyncio
import platform
from functools import reduce

import aiohttp
import aiostream

from ..common import batch_response_parsing
from ..modelling import Proxy
from ..repository import URL_freesources, URL_sanity, abc_Repository


# https://github.com/MagicStack/uvloop/issues/14
if platform.system().lower() != "windows":
    import uvloop

    #
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
else:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def _batch_download(session: aiohttp.ClientSession, endpoint: str) -> set[Proxy]:
    """downloads batch of proxy addresses from a free public source"""
    try:
        async with session.get(endpoint) as response:
            if response.status != 200:
                return set()

            response = await response.text()
    except asyncio.TimeoutError:
        return set()

    available = batch_response_parsing(response)

    return available


async def _is_proxy_working(
    session: aiohttp.ClientSession, proxy: Proxy, timeout: float = 5.0
) -> bool:
    """If proxy address is reachable and working"""
    try:
        async with session.get(
            URL_sanity.format(scheme=proxy.scheme),
            proxy=f"http://{proxy.peername}",
            allow_redirects=False,
            timeout=timeout,
        ) as response:
            peername = response.connection.transport.get_extra_info("peername")

            if not peername:
                return False

            return peername[0] == proxy.host
    except (
        AttributeError,
        aiohttp.ClientError,
        asyncio.TimeoutError,
    ):
        return False


class Repository(abc_Repository):
    def batch_download(self) -> set[Proxy]:
        return asyncio.run(self._batch_download())

    def reachability(self, available: set[Proxy]) -> tuple[set[Proxy], set[Proxy]]:
        return asyncio.run(self._reachability(available))

    async def _batch_download(self) -> set[Proxy]:
        timeout = aiohttp.ClientTimeout(
            sock_connect=self._timeout, sock_read=self._timeout
        )

        async with aiohttp.ClientSession(timeout=timeout) as session:
            available = await asyncio.gather(
                *[_batch_download(session, endpoint) for endpoint in URL_freesources]
            )

        available = reduce(lambda x, y: x | y, available)
        return available

    async def _reachability(
        self, available: set[Proxy]
    ) -> tuple[set[Proxy], set[Proxy]]:
        timeout = aiohttp.ClientTimeout(
            sock_connect=self._timeout, sock_read=self._timeout
        )

        positive = set()
        negative = set()

        batchsize = self._batchsize if self._batchsize > 0 else len(available)
        batchsize = min(batchsize, len(available))

        async with aiohttp.ClientSession(timeout=timeout) as session:
            iterator = aiostream.stream.iterate(available)
            iterator = aiostream.stream.chunks(iterator, batchsize)

            async with iterator.stream() as chunkset:
                async for batchset in chunkset:
                    response = await asyncio.gather(
                        *[
                            _is_proxy_working(session, proxy, self._timeout)
                            for proxy in batchset
                        ]
                    )

                    for x in zip(response, batchset):
                        positive.add(x[1]) if x[0] else negative.add(x[1])

        return positive, negative
