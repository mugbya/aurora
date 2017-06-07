from sanic import Sanic
import asyncio_redis
from aurora.view import bp
from aurora.user_views import bp as user_bp
from aurora.db import setup_connection, close_connection
from aurora.config import settings
from aurora.session import Session

app = Sanic(__name__)
session = Session()

session.init_app(app)

app.blueprint(bp)
app.blueprint(user_bp)

app.static('/static', settings.STATIC_URL)


@app.listener('after_server_start')
async def start_connection(app, loop):
    '''
    将数据库连接池放入blueprint
    :param app:
    :param loop:
    :return:
    '''
    _data_pool = await setup_connection(app, loop)
    bp.pool = _data_pool


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    await app.session_interface.open(request)

#
# @app.middleware('response')
# async def save_session(request, response):
#     # after each request save the session,
#     # pass the response to set client cookies
#     await session.save(request, response)


@app.middleware('request')
async def check_cookie(request):
    pass
    # await session.open(request)

if __name__ == "__main__":
    '''
    sanic 启动时创建数据库连接池，服务正常结束时关闭连接池
    '''
    # session = RedisSessionInterface(redis_getter=startup_redis_pool)

    app.run(host="127.0.0.1", port=settings.PORT, workers=settings.workers, debug=settings.DEBUG)

