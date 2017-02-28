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
    obj_list = await User.all()
    return json(obj_list)


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
    pass
    # if request.form:
    #     username = request.parsed_form.get('username', '')
    #     nickname = request.parsed_form.get('nickname', '')
    #     password = request.parsed_form.get('password', '')
    #     email = request.parsed_form.get('email', '')
    #
    #     async with conn_pool.acquire() as conn:
    #         try:
    #             result = await conn.execute(
    #                 '''INSERT INTO PUBLIC.user (username, nickname, password, email)
    #                     VALUES ('{username}', '{nickname}', '{password}', '{email}') '''.format(
    #                     username=username, nickname=nickname, password=password, email=email))
    #         except InvalidTextRepresentationError as e:
    #             client.captureException()
    #         except Exception as e:
    #             client.captureException()
    #
    #     if result:
    #         return json({'msg': 'ok'})
    #
    # return json({'msg': 'fail'})
