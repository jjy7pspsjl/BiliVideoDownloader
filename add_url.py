# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/12/12 13:43
# software : PyCharm
"""Add url to redis program."""

import time
import chardet
import aiohttp
import asyncio

from parse_ import parseUrl
from redisConnent import Redis
from config import HeadersConfig, UrlConfig


class AddUrlToRedis:
    """Add url to redis."""
    redis = None
    url_count = int()

    async def fetch(self, session, url, _json=False):
        async with session.get(url=url, headers=HeadersConfig.HEADERS) as resp:
            if _json:
                return await resp.json()
            encoding = chardet.detect(await resp.read())['encoding']
            return await resp.text(encoding=encoding, errors='ignore')

    async def set_to_redis(self, categroy: str, html):
        urls = await parseUrl(html)
        for url in urls:
            # If it does not exist 'All' set,  it is inserted into 'Urls' set.
            if not await self.redis.sismember('All', url + categroy):
                self.url_count += 1
                self.redis.sadd('Urls', url + categroy)
            # data persistence
            self.redis.sadd('All', url + categroy)

    async def main(self, redis):
        self.redis = redis
        async with aiohttp.ClientSession() as session:
            for category, urls in UrlConfig.ITEMS_URLS.items():
                tasks = [
                    asyncio.create_task(self.fetch(session, url, _json=True)) if 'region' in url
                    else asyncio.create_task(self.fetch(session, url)) for url in urls
                ]
                done, pending = await asyncio.wait(tasks)
                tasks = [asyncio.create_task(self.set_to_redis(category, data.result())) for data in done]
                await asyncio.wait(tasks)


async def start_work():
    start_time = time.time()
    addUrl = AddUrlToRedis()
    redis = Redis()
    _redis = await redis.set_redis_pool(address=('127.0.0.1', 6379), encoding='utf-8')
    await addUrl.main(_redis)
    await redis.close()
    print('共添加 %s 个url，共耗时：%s秒' % (addUrl.url_count, round(time.time() - start_time, 4)))
    #
    for i in range(3000, -1, -1):
        print(f'\r---在 {i} 秒之后，再次添加 url---', end='', flush=True)
        await asyncio.sleep(1)


if __name__ == '__main__':
    while True:
        asyncio.run(start_work())
