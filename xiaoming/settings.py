#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.settings
    ~~~~~~~~~~~~~~~~~~~~

    the global config of xiaoming application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
import os

DEBUG = True
COOKIE_SECRET = 'WSES27DmRCyHtsKDBvwvZ9Mrm14Uwk9VttZ/fCDHAAc='
# LOGIN_URL = '/login'
XSRF_COOKIES = True
THEME_NAME = 'simple'

# default templates and static path settings
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'templates')
STATIC_PATH = os.path.join(os.path.dirname(__file__), 'static')


DEFAULT_LOCALE = 'en_US' #'zh_CN'

# REDIS_SERVER = False

# If set to None or 0 the session will be deleted when the user closes the browser.
# If set number the session lives for value days.
PERMANENT_SESSION_LIFETIME = 1 # days

# redis connection config
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# mongodb setting
MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

try:
    from local_settings import *
except:
    pass