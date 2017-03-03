from sanic.response import json
from sanic import Blueprint
from sanic import Sanic
from aurora.models import User
from aurora.config import settings

from aurora.db import setup_connection, close_connection

import logging
logger = logging.getLogger()

app = Sanic(__name__)
bp = Blueprint('user', url_prefix='/v1/user')

'''
test pool 的服务端代码
'''


@bp.post('/test_login/')
async def test_login(request):
    '''
    服务端测试代码
    测试 并发数据库连接池情况
    :param request:
    :return:
    '''
    if request.method == 'POST':
        username = request.json.get('username', '')
        user_list = await User.filter(nickname=username)
        if user_list:
            response = json(user_list)
            return response
        else:
            return json({'msg': 'user not exist'})


if __name__ == "__main__":
    '''
    sanic 启动时创建数据库连接池，服务正常结束时关闭连接池
    '''
    app.blueprint(bp)
    app.run(host="0.0.0.0", port=settings.PORT, workers=settings.workers, debug=settings.DEBUG,
            after_start=setup_connection, after_stop=close_connection)
