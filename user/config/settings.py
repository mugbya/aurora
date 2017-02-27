# -*- coding: utf-8 -*-
"""
project settings for Aurora.

"""
import logging
from logging.config import dictConfig

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
        'f': {'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
    },
    handlers={
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG
              },
        'l': {
            'class': 'logging.StreamHandler',
            'formatter': 'f',
            'level': logging.INFO
        },

    },
    loggers={
        'root': {'handlers': ['l'],
                 'level': logging.DEBUG
                 }
    }
)

dictConfig(logging_config)

try:
    from .local_settings import *
except ImportError:
    pass
