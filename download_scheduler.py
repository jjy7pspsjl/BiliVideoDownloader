# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/12/12 13:43
# software : PyCharm

import re
import time
import chardet
import aiohttp
import asyncio

from parse_ import parseHtml
from config import HeadersConfig, UrlConfig
from download_stream_file import downloadStream
from merge_stream_file import mergeStreamFile


class DownloadStreams:
    """Download Bili video."""
    url = None
    size = None
    _type = None
    fileName = None

    async def fetch(self, session, url, _json=False):
        """Request url."""
        if not _json:
            url, categroy = url[:-3], UrlConfig.RANKING_DICT[url[-3:]]
            print('\r', categroy, url)
        async with session.get(url=url, headers=HeadersConfig.HEADERS) as resp:
            if _json:
                return await resp.json()
            encoding = chardet.detect(await resp.read())['encoding']
            encoding = 'utf-8' if encoding == 'Windows-1254' else encoding
            fileName, videoUrl, audioUrl = await parseHtml(await resp.text(encoding=encoding, errors='ignore'))
            fileName = re.sub(r'[?*/\\|.:><]', '', fileName)
            return categroy, fileName, videoUrl, audioUrl

    async def get_urls(self, session, count: int = 1):
        """If the url is empty, wait for 300 seconds and request again."""
        get_urls = f'http://localhost:8080/get_url?count={count}'
        urls = await self.fetch(session, get_urls, _json=True)
        if not urls:
            for i in range(1000, -1, -1):
                print(f'\r---暂时没有URL啦, 休息 {i} 秒再来试试吧---', end='', flush=True)
                await asyncio.sleep(1)
        task_getUrl = [asyncio.create_task(self.fetch(session, UrlConfig.URL_HEAD + url)) for url in
                       urls] if urls else await self.get_urls(session, count)
        return task_getUrl

    async def get_streamFile_details(self, session, url, categroy, fileName):
        """get streamFile size."""
        HeadersConfig.VIDEO_HEADERS['range'] = 'bytes=0-10'
        async with session.get(url=url, headers=HeadersConfig.VIDEO_HEADERS,) as resp:
            fileSize = re.findall('bytes 0-10/(\d+)', dict(resp.headers)['Content-Range'])[0]
            _type = fileName[-4:]
            fileName = fileName[:-4]
            if int(fileSize) > 1073741824:
                return None
            return categroy, fileSize, fileName, _type, url

    async def main(self, count: int = 1):
        urls = [
            'BV1dK411G765208',
        #     'BV1ZV411y75g208',
        #     'BV1ea4y1e7Tf208',
        #     'BV1UC4y1t7EL208',
        #     'BV1Ka4y1i7Pz208'
        ]
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False),
                                         headers={'Connection': 'keep-alive'},
                                         trust_env=True,
                                         ) as session:
            task_getUrl = [asyncio.create_task(self.fetch(session, UrlConfig.URL_HEAD + url)) for url in
                           urls] if urls else await self.get_urls(session, count)
            # task_getUrl = await self.get_urls(session, count)
            done, pending = await asyncio.wait(task_getUrl)
            #
            task_merge_streamFile = list()  # Task queue, merge_streamFile
            task_streamFile_details = list()  # Task queue, get streamFile details
            for result in done:
                categroy, fileName, videoUrl, audioUrl = result.result()
                task_merge_streamFile.append([fileName, categroy])
                task_streamFile_details.append(asyncio.create_task(self.get_streamFile_details(session, videoUrl, categroy, f'{fileName}.m4s')))
                task_streamFile_details.append(asyncio.create_task(self.get_streamFile_details(session, audioUrl, categroy, f'{fileName}.mp3')))
            done, pending = await asyncio.wait(task_streamFile_details)
            # Task queue, download
            task_download = list()
            for data in done:
                print(data.result())
                categroy, size, fileName, _type, url = data.result()
                task_download.append(asyncio.create_task(downloadStream(url=url, size=size, fileName=fileName, _type=_type, categroy=categroy)))
            await asyncio.wait(task_download)
            # Delete the files before the merge.
            for data in task_merge_streamFile:
                await mergeStreamFile(*data)


async def start_download(count: int = 1):
    ds = DownloadStreams()
    await ds.main(count)

if __name__ == '__main__':
    while True:
        start_time = time.time()
        asyncio.run(start_download())
        print(time.time() - start_time)
        break
