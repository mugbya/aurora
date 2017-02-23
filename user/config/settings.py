# -*- coding: utf-8 -*-
"""
settings for ull_user project.

"""


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

try:
    from .local_settings import *
except ImportError:
    pass