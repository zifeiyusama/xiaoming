#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming
    ~~~~~~~~~~~~~~~~~~~~

    xiaoming Application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
import os
import redis
import tornado.web
import logging

from xiaoming import settings as config
from xiaoming.helpers import setting_from_object
from xiaoming.extensions.routing import Route
from xiaoming.extensions.session import RedisSessionStore

from xiaoming import views

class Application(tornado.web.Application):

    def __init__(self):
        settings = setting_from_object(config)
        handlers = [] + Route.routes()

        tornado.web.Application.__init__(self, handlers, **settings)

        pool = redis.ConnectionPool(host=settings['redis_host'], port=settings['redis_port'], db=settings['redis_db'])
        self.redis = redis.Redis(connection_pool=pool)
        self.session_store = RedisSessionStore(self.redis)