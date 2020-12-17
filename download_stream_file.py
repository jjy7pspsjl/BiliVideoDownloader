# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/12/12 13:43
# software : PyCharm

import asyncio
import aiohttp
import aiofiles

from config import PathConfig, HeadersConfig


class DownloadStream:
    """download stream file."""
    url = None
    size = None
    _type = None
    fileName = None
    categroy = None

    async def download_stream(self, session, fileName, _range):
        HeadersConfig.VIDEO_HEADERS['range'] = _range
        async with session.get(url=self.url, headers=HeadersConfig.VIDEO_HEADERS) as resp:
            async with aiofiles.open(fileName, 'wb') as afp:
                await afp.write(await resp.read())

    async def set_download_task(self, session):
        """set download task."""
        tasks = list()
        chunk, _index = int(), int()
        # Each file size is 10MB
        for size in range(10485760, self.size + 1, 10485760):
            start_chunk = chunk if chunk else -1
            if chunk + 10485760 > self.size:
                break
            chunk += 10485760
            fileName = f'{PathConfig.FILE_PATH}\\{self.categroy}\\{self.fileName}{_index}{self._type}'
            _range = f'bytes={start_chunk + 1}-{chunk}'
            tasks.append(asyncio.create_task(self.download_stream(session, fileName, _range)))
            _index += 1
        # Final download
        chunk = chunk if chunk else -1
        fileName = f'{PathConfig.FILE_PATH}\\{self.categroy}\\{self.fileName}{_index}{self._type}'
        _range = f'bytes={chunk + 1}-{self.size - 1}'
        tasks.append(asyncio.create_task(self.download_stream(session, fileName, _range)))
        return tasks

    async def main(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.size = int(kwargs.get('size'))
        self._type = kwargs.get('_type')
        self.categroy = kwargs.get('categroy')
        self.fileName = kwargs.get('fileName')
        async with aiohttp.ClientSession(headers={'Connection': 'keep-alive'}) as session:
            done = await self.set_download_task(session=session)
            await asyncio.wait(done, timeout=180)


async def downloadStream(url: str, size: str, fileName: str, _type: str, categroy: str):
    _download = DownloadStream()
    await _download.main(url=url, size=size, fileName=fileName, _type=_type, categroy=categroy)
