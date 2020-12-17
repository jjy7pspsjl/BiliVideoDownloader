# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/12/12 15:41
# software : PyCharm

import os
import asyncio
import aiofiles
import subprocess

from config import PathConfig


class MergeStreamFile:
    """Merge stream file."""
    Lock = None
    path = None
    categroy = None
    fileName = None

    async def merge_file(self):
        # This is where the files are stored,get file count.
        _types = ['m4s', 'mp3']
        fileList = os.listdir(self.path)
        for _type in _types:
            fileCount = int()
            for file in fileList:
                if self.fileName + _type == file:
                    continue
                if self.fileName in file and _type in file:
                    fileCount += 1
            if fileCount:
                async with aiofiles.open(f'{self.path}\\{self.fileName}.{_type}', 'wb') as afp:
                    for index in range(fileCount):
                        await self.Lock.acquire()
                        async with aiofiles.open(f'{self.path}\\{self.fileName}{index}.{_type}', 'rb') as f:
                            await afp.write(await f.read())
                            await f.close()
                        self.Lock.release()
                        await self.delete_stream_file(fileName=f'{self.path}\\{self.fileName}{index}.{_type}')
                    await afp.close()

    async def merge_video_audio(self):
        """merge video and audio."""
        await self.Lock.acquire()
        command = f'{PathConfig.FFMPEG_PATH} -i "{self.path}\\{self.fileName}.m4s" -i ' \
                  f'"{self.path}\\{self.fileName}.mp3" -c copy "{self.path}\\{self.fileName}.mp4" -loglevel quiet -n'
        subprocess.Popen(command, shell=True)
        await asyncio.sleep(2.5)
        self.Lock.release()
        print(f'{self.fileName}.mp4合并完成！！！')
        # await self.delete_stream_file(f"{self.path}\\{self.fileName}.m4s")  # delete stream file
        # await self.delete_stream_file(f"{self.path}\\{self.fileName}.mp3")  # delete stream file

    async def delete_stream_file(self, fileName: str):
        """delete stream file."""
        filePath = fileName
        if os.path.exists(filePath):
            os.remove(filePath)

    async def main(self, **kwargs):
        self.fileName = kwargs.get('fileName')
        self.categroy = kwargs.get('categroy')
        self.Lock = asyncio.Lock()
        self.path = f"{PathConfig.FILE_PATH}\\{self.categroy}"
        await self.merge_file()
        await self.merge_video_audio()
        await asyncio.sleep(1)
        await self.delete_stream_file(f"{self.path}\\{self.fileName}.m4s")
        await self.delete_stream_file(f"{self.path}\\{self.fileName}.mp3")


async def mergeStreamFile(fileName: str, categroy: str):
    msf = MergeStreamFile()
    await msf.main(fileName=fileName, categroy=categroy)
