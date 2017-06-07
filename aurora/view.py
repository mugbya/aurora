import binascii
import os
import logging
from sanic.response import text, html, json, redirect
from sanic.blueprints import Blueprint
from aurora.util.sanic_jinja import render
from aurora.models import User

bp = Blueprint('base_user')


logger = logging.getLogger(__name__)


@bp.get('/')
async def index(request):
 
    user = request.user
    return render('index.html', request, user=user)





