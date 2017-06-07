import os
from sanic_session import RedisSessionInterface, MemcacheSessionInterface
from sanic_session.base import BaseSessionInterface
from aurora.config import settings
import asyncio_redis
from aurora.view import bp


class NullSessionInterface(BaseSessionInterface):
    """Used to open a :class:`flask.sessions.NullSession` instance.
    """

    def open_session(self, app, request):
        return None


async def startup_redis_pool():
    # redis
    _redis_pool = await asyncio_redis.Pool.create(**settings.SESSION)
    bp.redis = _redis_pool
    return _redis_pool


class Session:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.session_interface = self._get_interface(app)

    def _get_interface(self, app):

        if settings.SESSION['session_type'] == 'redis':
            session_interface = RedisSessionInterface(redis_getter=startup_redis_pool)
        elif settings.SESSION['session_type'] == 'memcached':
            session_interface = MemcacheSessionInterface()
        else:
            session_interface = NullSessionInterface()

        return session_interface

