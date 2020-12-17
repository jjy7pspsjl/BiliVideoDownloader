# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/12/12 13:00
# software : PyCharm

import json
import time
import asyncio

from create_folder import CreateFolder
from download_scheduler import start_download


def get_argument():
    with open('working.json', 'r', encoding='utf-8') as f:
        _dict = json.load(f)
        stop = _dict["stop"]
        count = _dict["count"]
    return stop, count


async def run(**kwargs):
    CreateFolder()  # create folder
    tasks = list()  # task list
    count = kwargs.get("count")
    # 每个任务下载多少个视频  count
    tasks.append(asyncio.create_task(start_download(count)))
    await asyncio.wait(tasks)


if __name__ == '__main__':
    stop, count = get_argument()
    while stop:
        start_time = time.time()
        asyncio.run(run(count=count))
        print(time.time() - start_time)
        stop, count = get_argument()
