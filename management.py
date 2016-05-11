#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.management
    ~~~~~~~~~~~~~~~~~~~~

    the management interface of xiaoming application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
from datetime import datetime
import logging
import pymongo

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from xiaoming import Application
import motor
from xiaoming.settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE, SOCKET_CLIENT_PARK_NUMBER
from xiaoming.socket import SocketClient

define("port", default=8000, help="run on the given port", type=int)
define("cmd", default='runserver', 
        metavar="runserver|createuser|runsocket",
        help=("Default use runserver"))


def main():
    tornado.options.parse_command_line()
    if options.cmd == "runserver":
        application = Application()
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port)
        application.check_appointment()
        tornado.ioloop.IOLoop.instance().start()
    elif options.cmd == "createuser":
        email = input("please enter a email as login username:\n")
        while email is None:
            email = input("please enter a email as login username:\n")
        client = pymongo.MongoClient("localhost", 27017)
        db = client['park']
        existed_admin = db.admin.find_one({'email': email})
        while existed_admin is not None:
            email = input("the email was already used, please choose another, or enter a 'q' to quit:\n")
            if email == "q":
                return
        password = input("please enter your password:\n")
        while password is None:
            password = input("please enter your password:\n")
        repeate_pwd = input("please repeat your password:\n")
        while repeate_pwd is None:
            repeate_pwd = input("please repeat your password:\n")
        while password != repeate_pwd:
            repeate_pwd = input("the two passwords you entered didn't match, please repeat again or enter a 'q' to quit:\n")
            if repeate_pwd =='q':
                return
        name = input("please enter your name\n")
        while name is None:
            input("please enter your name\n")
        admin = {
            'email': email,
            'name': name,
            'password': password,
            'created_date': datetime.utcnow()
        }
        db.admin.insert(admin)
    elif options.cmd == "runsocket":
        db = get_db()
        import socket
        HOST = socket.gethostname()
        PORT = 50001
        park_number = 'P201605041516388'
        io_loop = tornado.ioloop.IOLoop.instance()
        socket_client = SocketClient(HOST, PORT, db, park_number, io_loop)
        socket_client.connect()
        io_loop.start()
    else:
        print("error cmd param: python3 management.py --help")

def get_db():
    client = motor.MotorClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DATABASE]
    return db

if __name__ == "__main__":
    main()
