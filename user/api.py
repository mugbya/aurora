from sanic.response import json
from sanic import Blueprint

from models import User

import logging

bp = Blueprint('user', url_prefix='/v1/user')


@bp.route('/')
async def index(request):
    '''
    获取所有用户列表
    :param request:
    :return:
    '''
    obj_list = await User.findAll()
    return json(obj_list)


@bp.route('/<username>/')
async def get_user(request, username):
    '''
    以用户名获取指定用户对象
    :param request:
    :return:
    '''

    user = await User.findAll('nickuser=?', [username])
    # async with conn_pool.acquire() as conn:
    #     stmt = await conn.prepare(
    #         '''SELECT id,  email FROM public.user WHERE nickname='{nickname}' '''.format(nickname=username, ))
    #
    #     results = await stmt.fetch()
    #
    # obj_list = [dict(obj) for obj in results]
    # return json(obj_list)


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
