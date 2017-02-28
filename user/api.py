from sanic.response import json
from sanic import Blueprint

from models import User

import logging

logger = logging.getLogger()

bp = Blueprint('user', url_prefix='/v1/user')

'''
/v1/user 旨在 以orm实现业务需求
'''


@bp.route('/')
async def index(request):
    '''
    获取所有用户列表
    :param request:
    :return:
    '''
    try:
        obj_list = await User.all()
        return json(obj_list)
    except Exception as e:
        logger.error('index error', str(e))
        return json({'msg': 'fail'})


@bp.route('/<username>/')
async def get_user(request, username):
    '''
    以用户名获取指定用户对象
    :param request:
    :return:
    '''
    try:
        user_list = await User.filter(nickname=username,)
        # user_list = await User.findAll('nickname=$1', username)

        return json(user_list)
    except Exception as e:
        logger.error('get_user error', str(e))
        return json({'msg': 'fail'})


@bp.post('/save/')
async def save_user(request):
    '''
    保存user对象
    :param request:
    :return:
    '''
    try:
        if request.form:
            username = request.parsed_form.get('username', '')
            nickname = request.parsed_form.get('nickname', '')
            password = request.parsed_form.get('password', '')
            email = request.parsed_form.get('email', '')

            user = User(username=username, nickname=nickname, password=password, email=email)
            res = await user.save()

            if res:
                return json({'msg': 'ok'})
        return json({'msg': 'fail'})

    except Exception as e:
        logger.error('user save error', str(e))
        return json({'msg': 'fail'})
