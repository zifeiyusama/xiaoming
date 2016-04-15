#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    management
    ~~~~~~~~~~~~~~~~~~~~

    the management interface of xiaoming application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
from datetime import datetime

import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado.options import define, options

from xiaoming import Application
from xiaoming.models import connection as con

define("port", default=8000, help="run on the given port", type=int)


def main():
    tornado.options.parse_command_line()
    if options.cmd == "runserver":
        http_server = tornado.httpserver.HTTPServer(Application())
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
    elif options.cmd == "createuser":
        email = input("please enter a email as login username")
        existed_admin = con.Admin.find_one({ "email": email})
        while existed_admin is not None:
            email = input("the email was already used, please choose another, or enter a 'q' to quit")
            if email == "q":
                break
        password = input("please enter your password")
        repeate_pwd = input("please repeat your password")
        while password != repeate_pwd:
            repeate_pwd = input("the two passwords you entered didn't match, please repeat again or enter a 'q' to quit")
            if repeate_pwd =='q':
                break
        name = input("please enter your name")
        admin = con.Admin()
        admin['email'] = email
        admin['name'] = name
        admin['password'] = password
        admin['created_date'] = datetime.utcnow
        admin.save()
    else:
        print("error cmd param: python3 management.py --help")

if __name__ == "__main__":
    main()
