#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming
    ~~~~~~~~~~~~~~~~~~~~

    views for xiaoming Application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
from tornado import gen
from xiaoming.extensions.request_handler import RequestHandler
from xiaoming.extensions.routing import route

from xiaoming.models import connection as con

@route(r'/login', name='login')
class Login(RequestHandler):

    def get(self):
        self.render('login.html')

    @gen.coroutine
    def post(self):
        email = self.get_body_argument("email", default="")
        password = self.get_body_argument("password", default="")
        user = yield con.Admin.find_one({ "email": email, "password":password })
        redirect_url = "/login"
        if user:
            self.session['user'] = user
            self.session.save()
            next_url = self.get_body_argument("next")
            redirect_url = next_url or "/"
            self.flash("登录成功","success")
        else:
            self.flash("登录失败","error")
        return self.redirect(redirect_url)


@route(r'/', name='index')
class Index(RequestHandler):

    def get(self):
        self.render('index.html')