import logging
from sanic.response import text, html, json
from jinja2 import Template, PackageLoader, Environment
from sanic.blueprints import Blueprint

from models import User

bp = Blueprint('view_user')

logger = logging.getLogger(__name__)


@bp.route('/login/', methods=['GET', 'POST'])
async def login(request):
    logger.debug('debug message')
    logger.info('info message')

    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')
    # if request.method == 'POST':
    #     username = request.form.get('username', '')
    #     password = request.form.get('password', '')
    #
    #     user = await User.filter(username=username, password=password)
    #     if user:
    #         print('sdfsd')
    #     return json({})
    # else:
    #     pass

