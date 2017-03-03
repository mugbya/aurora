from sanic import Sanic

from api import bp as user_bp
from api_v2 import bp as user_v2_bp
from view import bp as view_bp
from db import setup_connection, close_connection
from config import settings

from sanic_session import InMemorySessionInterface

app = Sanic(__name__)
session = InMemorySessionInterface(cookie_name=app.name, prefix=app.name)

app.blueprint(user_bp)
app.blueprint(user_v2_bp)
app.blueprint(view_bp)
app.static('/static', './static')


@app.middleware('request')
async def add_session_to_request(request):
    # before each request initialize a session
    # using the client's request
    await session.open(request)


@app.middleware('response')
async def save_session(request, response):
    # after each request save the session,
    # pass the response to set client cookies
    await session.save(request, response)


async def start_connection(app, loop):
    '''
    将数据库连接池放入blueprint
    :param app:
    :param loop:
    :return:
    '''
    _pool = await setup_connection(app, loop)
    view_bp.pool = user_v2_bp.pool = _pool


if __name__ == "__main__":
    '''
    sanic 启动时创建数据库连接池，服务正常结束时关闭连接池
    '''
    app.run(host="0.0.0.0", port=settings.PORT, workers=settings.workers, debug=settings.DEBUG,
            after_start=start_connection, after_stop=close_connection)
