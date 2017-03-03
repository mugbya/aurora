# -*- coding: utf-8 -*-
"""
project settings for Aurora.

"""
import os
import logging
from logging.config import dictConfig

# BASE_DIR = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PACKAGE_NAME = os.path.basename(os.getcwd())

STATIC_URL = '/static/'
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
            'filename': '../log/all.log',
            'formatter': 'default',
            'level': logging.INFO
        },
    },
    loggers={
        'sanic': {
            'handlers': ['file'],
            'level': logging.INFO,
            "encoding": "utf8"
        },
        'db': {
            'handlers': ['file'],
            'level': logging.INFO,
            "encoding": "utf8"
        },
        'view': {
            'handlers': ['file'],
            'level': logging.INFO,
            "encoding": "utf8"
        },
    }
)

dictConfig(logging_config)

try:
    from .local_settings import *
except ImportError:
    pass
