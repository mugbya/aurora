from sanic.response import json
from sanic import Blueprint

import asyncpg

from asyncpg.exceptions import InvalidTextRepresentationError

from config import settings

bp = Blueprint('user', url_prefix='/v1/user')


@bp.listener('before_server_start')
async def setup_connection(app, loop):
    global conn_pool
    conn_pool = await asyncpg.create_pool(**settings.DB_CONFIG)


@bp.listener('after_server_stop')
async def close_connection(app, loop):
    await conn_pool.close()


@bp.route('/')
async def index(request):
    '''
    获取所有用户列表
    :param request:
    :return:
    '''
    async with conn_pool.acquire() as conn:
        stmt = await conn.prepare('''SELECT id, username, email FROM public.user''')
        results = await stmt.fetch()

    obj_list = [dict(obj) for obj in results]
    return json(obj_list)


@bp.route('/<username>/')
async def get_user(request, username):
    '''
    以用户名获取指定用户对象
    :param request:
    :return:
    '''
    async with conn_pool.acquire() as conn:
        stmt = await conn.prepare(
            '''SELECT id,  email FROM public.user WHERE nickname='{nickname}' '''.format(nickname=username, ))

        results = await stmt.fetch()

    obj_list = [dict(obj) for obj in results]
    return json(obj_list)


@bp.post('/save/')
async def save_user(request):
    '''
    保存user对象
    :param request:
    :return:
    '''
    if request.form:
        username = request.parsed_form.get('username', '')
        nickname = request.parsed_form.get('nickname', '')
        password = request.parsed_form.get('password', '')
        email = request.parsed_form.get('email', '')

        async with conn_pool.acquire() as conn:
            try:
                result = await conn.execute(
                    '''INSERT INTO PUBLIC.user (username, nickname, password, email)
                        VALUES ('{username}', '{nickname}', '{password}', '{email}') '''.format(
                        username=username, nickname=nickname, password=password, email=email))
            except InvalidTextRepresentationError as e:
                # TODO log handler
                print('insert error:', e.message)
            except Exception as e:
                print('error:', e.message)

        if result:
            return json({'msg': 'ok'})

    return json({'msg': 'fail'})
