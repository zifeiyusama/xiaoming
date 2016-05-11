#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.socket
    ~~~~~~~~~~~~~~~~~~~~

    the socket module interacting with sensers

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""

import socket

import tornado.ioloop
import tornado.iostream
from tornado import gen
from tornado.concurrent import Future

from datetime import datetime
import logging
import time
import json

from xiaoming.helpers import init_update

class SocketClient(object):
    """The socketclient used to interact with the socket server
    in the sensor
    """

    def __init__(self, host, port, db, park_number, ioloop=None):
        self.host = host
        self.port = port
        self.stream = None
        self.ioloop = ioloop
        self.db = db
        self.park_number = park_number

    def _get_stream(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(s)

    @gen.coroutine
    def _store_data(self, data):
        logging.info(data)
        datas = json.loads(bytes.decode(data))
        logging.info(datas)
        bulk = self.db.carport.initialize_ordered_bulk_op()
        formated_data = datas['datas']
        for d in formated_data:
            sensors = {"number":d["SID"], "status": d["STATE"]}
            status = 'FREE'
            if d["STATE"] == '1':
                status = 'OCCUPIED'
            bulk.find({'number': d['CID']}).update(
                {
                    '$set':
                    {
                        'sensors': sensors,
                        'last_modified_date': datetime.utcnow(),
                        'last_modified_by': '',
                        'status': status
                    }
                }
            )
        result = yield bulk.execute()
        self._handle_data()

    def _get_data(self):
        future = Future()
        logging.info('client begin get_data')
        data = self.stream.read_until_regex(b']}$', self._store_data)
        future.set_result(data)
        return future

    @gen.coroutine
    def _handle_data(self):
        logging.info('client begin handle_data')
        yield self._get_data()

    def connect(self):
        self._get_stream()
        logging.info('client begin connect')
        self.stream.connect((self.host, self.port), self._handle_data)


