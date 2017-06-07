# -*- coding: utf-8 -*-
"""
project settings for Aurora.

"""
import os
import logging
from logging.config import dictConfig

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE_NAME = os.path.basename(os.getcwd())

STATIC_URL = 'webContent/static'
TEMPLATES = "webContent/templates"

DEBUG = False

workers = 4

PORT = 80


DB_CONFIG = {
    'host': '<host>',
    'user': '<username>',
    'password': '<password>',
    'port': '<port>',
    'database': '<database>'
}

# session 配置
SESSION = {
    'session_type': 'redis',
    'host': '127.0.0.1',
    'port': '6379',
}


'''
日志集成器
'''
# from raven import Client
# client = Client('https://******@sentry.io/141953')


'''
python自带日志
'''
logging_config = dict(
    version=1,
    formatters={
        'default': {
            'format': '%(asctime)s %(levelname)-8s %(name)-15s %(message)s'
        }
    },
    filter={
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': logging.INFO
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR + '/log/all.log',
            'formatter': 'default',
            'level': logging.INFO,
        },
    },
    loggers={
        '': {
            'handlers': ['file'],
            'level': logging.INFO,
            "encoding": "utf8",
            'propagate': True
        },
        'sanic': {
            'handlers': ['file'],
            'level': logging.INFO,
            "encoding": "utf8",
            'propagate': True
        },
        'db': {
            'handlers': ['file'],
            'level': logging.INFO,
            "encoding": "utf8"
        },
        'view': {
            'handlers': ['file'],
            'level': logging.INFO,
            "encoding": "utf8",
            'propagate': True
        },
    }
)
dictConfig(logging_config)

try:
    from .local_settings import *
except ImportError:
    pass
