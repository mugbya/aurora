import logging
from sanic.response import text, html, json
from sanic.blueprints import Blueprint
from aurora.util.sanic_jinja import render
from aurora.models import User

bp = Blueprint('view_user')


logger = logging.getLogger(__name__)


@bp.route('/login/', methods=['GET', 'POST'])
async def login(request):
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        user_list = await User.filter(nickname=username, password=password)
        if user_list:
            response = json(user_list)
            response.cookies[username] = username
            response.cookies[username]['domain'] = '.gotta-go-fast.com'
            response.cookies[username]['httponly'] = True
            return response

            # return json(user_list)
        else:
            return json({'msg': 'user not exist'})
    else:
        return render('login.html', request)


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
