# -*- coding:utf-8 -*-
# author   : SunriseCai
# datetime : 2020/12/12 13:43
# software : PyCharm


from sanic import Sanic
from sanic import response

from redisConnent import Redis

app = Sanic(__name__)


@app.route("/get_url")
async def handle(request):
    print(request.args.get('count'))
    count = int(request.args.get('count'))
    redis = request.app.redis
    urls_list = list()
    while len(urls_list) < count:
        url = await redis.srandmember('Urls')  # get url
        if url:
            urls_list.append(url)  # add url to urls_list
            redis.srem('Urls', url)  # delete url in redis
        else:
            break
    return response.json(body=urls_list)


@app.listener('before_server_start')  # before server start
async def before_server_start(app, loop):
    _redis = Redis()
    # redis connect pool
    app.redis = await _redis.set_redis_pool(address=('127.0.0.1', 6379), encoding='utf-8')


@app.listener('after_server_stop')  # after server stop
async def after_server_stop(app):
    app.redis.close()


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        # host="127.0.0.1",
        port=8080,  # default 8080
    )
