# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/12/10 8:02
# software : PyCharm

"""Redis connect."""

import aioredis


class Redis:
    ...
    _redis = None

    async def set_redis_pool(self, *args, **kwargs):
        if not self._redis:
            self._redis = await aioredis.create_redis_pool(*args, **kwargs)
        return self._redis

    async def close(self):
        await self._redis.unsubscribe('chan:1')
        if self._redis:
            self._redis.close()
