from sanic.response import json
from sanic import Blueprint

import logging

logger = logging.getLogger()

bp = Blueprint('user_v2', url_prefix='/v2/user')

'''
/v2/user 旨在 以原生sql实现业务需求

'''


@bp.route('/')
async def index(request):
    '''
    获取所有用户列表
    :param request:
    :return:
    '''
    try:
        async with bp.pool.acquire() as conn:
            stmt = await conn.prepare('''SELECT id,  email FROM users ''')

            results = await stmt.fetch()

        obj_list = [dict(obj) for obj in results]
        return json(obj_list)
    except Exception as e:
        logger.error('index error', e)
        return json({'msg': 'fail'})


@bp.route('/<username>/')
async def get_user(request, username):
    '''
    以用户名获取指定用户对象
    :param request:
    :return:
    '''
    try:
        async with bp.pool.acquire() as conn:
            sql = '''SELECT id,  email FROM users WHERE nickname='{nickname}' '''.format(nickname=username, )
            stmt = await conn.prepare(sql)
            results = await stmt.fetch()

        obj_list = [dict(obj) for obj in results]
        return json(obj_list)
    except Exception as e:
        logger.error('index error', e)
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

            async with bp.pool.acquire() as conn:
                sql = '''INSERT INTO PUBLIC.user (username, nickname, password, email)
                        VALUES ('{username}', '{nickname}', '{password}', '{email}') '''.format(
                        username=username, nickname=nickname, password=password, email=email)
                result = await conn.execute(sql)
            if result:
                return json({'msg': 'ok'})

        return json({'msg': 'fail'})

    except Exception as e:
        logger.error('index error', e)
        return json({'msg': 'fail'})
