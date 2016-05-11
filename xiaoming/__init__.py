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
from tornado import gen

from xiaoming import settings as config
from xiaoming.helpers import setting_from_object
from xiaoming.extensions.routing import Route
from xiaoming.extensions.session import RedisSessionStore
from xiaoming.views import *
from xiaoming.api import *
import logging
from datetime import datetime
import time

import motor

class Application(tornado.web.Application):

    def __init__(self):
        settings = setting_from_object(config)
        handlers = [] + Route.routes()

        client = motor.MotorClient(settings['mongo_host'], settings['mongo_port'])
        self.database = client[settings['mongo_database']]

        pool = redis.ConnectionPool(host=settings['redis_host'], port=settings['redis_port'], db=settings['redis_db'])
        self.redis = redis.Redis(connection_pool=pool)
        self.session_store = RedisSessionStore(self.redis)
        tornado.web.Application.__init__(self, handlers, **settings)

    @gen.coroutine
    def check_appointment(self):
        timeline = datetime.utcnow()
        logging.info('find appointment ..')
        result = yield self.database.park.update(
            {
                'is_appointment': True,
                'appointment_date':{'$gte':timeline},
                'status':'OPEN'
            },
            {'$set': {'status':'OVERDUE'}}
        )
        yield gen.sleep(60)
        self.check_appointment()