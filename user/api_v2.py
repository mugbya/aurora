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
        async with bp.pool.acquire() as conn:
            # 使用格式化
            # sql = '''SELECT id,  email FROM users WHERE nickname='{nickname}' '''.format(nickname=username, )
            # stmt = await conn.prepare(sql)
            # results = await stmt.fetch()

            # 使用 asyncpg 提供的占位符
            sql = '''SELECT id,  email FROM users WHERE nickname=$1 '''
            stmt = await conn.prepare(sql)
            results = await stmt.fetch(username)

        obj_list = [dict(obj) for obj in results]
        return json(obj_list)
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

            async with bp.pool.acquire() as conn:

                # sql = '''INSERT INTO users (username, nickname, password, email)
                #         VALUES ('{username}', '{nickname}', '{password}', '{email}') '''.format(
                #         username=username, nickname=nickname, password=password, email=email)
                # result = await conn.execute(sql)

                sql = '''INSERT INTO users (username, nickname, password, email) VALUES ($1, $2, $3, $4) '''
                result = await conn.execute(sql, username, nickname, password, email)
            if result:
                return json({'msg': 'ok'})

        return json({'msg': 'fail'})

    except Exception as e:
        logger.error('user save error', str(e))
        return json({'msg': 'fail'})
