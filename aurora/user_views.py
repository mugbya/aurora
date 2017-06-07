import binascii
import os
import logging
from sanic.response import text, html, json, redirect
from sanic.blueprints import Blueprint
from aurora.util.sanic_jinja import render
from aurora.models import User

bp = Blueprint('user_view', url_prefix='user')


logger = logging.getLogger(__name__)


@bp.route('/login/', methods=['GET', 'POST'])
async def login(request):
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        user_list = await User.filter(nickname=username, password=password)
        if user_list:
            _token = binascii.hexlify(os.urandom(16)).decode("utf8")
            response = json(_token)

            # if not request._cookies.get('session'):
            #     request['session']['session'] = _token
            # return response

        else:
            return json({'msg': 'user not exist'})
    else:
        return render('login.html', request)


@bp.route('/list/', methods=['GET'])
async def login(request):
    if request.method == 'GET':

        user_list = await User.all()
        if user_list:
           return json(user_list)
        else:
            return json({'msg': 'user not exist'})
    else:
        return render('login.html', request)