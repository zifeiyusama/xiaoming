#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.views
    ~~~~~~~~~~~~~~~~~~~~

    views for xiaoming Application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
import json
from tornado import gen
import tornado.web

from xiaoming.extensions.request_handler import RequestHandler
from xiaoming.extensions.routing import route
from xiaoming.helpers import init_insert

from datetime import datetime
import logging

from bson.objectid import ObjectId


@route(r'/login', name='login')
class LoginHandler(RequestHandler):

    def get(self):
        self.render('login.html')

    @gen.coroutine
    def post(self):
        email = self.get_body_argument("email", default="")
        password = self.get_body_argument("password", default="")
        user = yield self.db.admin.find_one({'email': email, 'password': password})
        redirect_url = "/login"
        if user:
            self.session['user'] = user
            print(self.session['user'])
            self.session.save()
            next_url = self.get_body_argument("next", default=None)
            redirect_url = next_url or "/"
            self.flash("登录成功","success")
        else:
            self.flash("登录失败","error")
        return self.redirect(redirect_url)


@route(r'/', name='index')
class IndexHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        return self.render('index.html')


@route(r'/parks', name='parks')
class ParksHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        result = []
        cursor = self.db.park.find().sort([('number', 1)])
        while (yield cursor.fetch_next):
            park = cursor.next_object()
            result.append(park)
        return self.render('park.html', parks=result)

    @gen.coroutine
    def post(self):
        # TODO: verify whether the user has logged in or not
        description = self.get_body_argument("description", default="")
        name = self.get_body_argument("name", default="")
        status = self.get_body_argument("status", default="PREPARING")
        park = {
            'description': description,
            'name': name,
            'status': status,
            'location':{},
            'carport_count': 0,
        }
        amdin = self.get_current_user()
        init_info = init_insert(namespace='P', user_id=ObjectId(amdin['_id']))
        park = yield self.db.park.insert(dict(park, **init_info))
        return self.redirect(self.reverse_url('parks'))

@route(r'/carports', name='carports')
class CarportHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        park_options = {}
        carports = []
        cursor = self.db.park.find()
        while (yield cursor.fetch_next):
            park = cursor.next_object()
            park_options[park['_id']] =  park['name']
        carport_cursor = self.db.carport.find()
        while(yield carport_cursor.fetch_next):
            doc = carport_cursor.next_object()
            carports.append(doc)
        return self.render('carport.html', park_options=park_options, carports=carports)

    @gen.coroutine
    def post(self):
        number = self.get_body_argument("number", default="")
        park = self.get_body_argument("park", default="")
        status = self.get_body_argument("status", default="")
        amdin = self.get_current_user()
        admin_id = ObjectId(amdin['_id'])
        park_id = ObjectId(park)
        init_info = init_insert(user_id=admin_id)
        carport_info = {
            "park_id": park_id,
            "number": number,
            "status": status,
            "sensors":{}
        }
        carport = yield self.db.carport.insert(dict(carport_info, **init_info))
        park = yield self.db.park.find_and_modify({
            "_id": park_id
        }, {
            "$inc": {"carport_count": 1}
        })
        return self.redirect(self.reverse_url('carports'))

# @route(r'/ajax_carport', name='ajax_carport')
# class AjaxCarportHandler(RequestHandler):

#     @gen.coroutine
#     def post(self):
#         carport_options = {}
#         park_id = self.get_body_argument("park")
#         logging.info("park_id is %s" % park_id)
#         if park_id != None:
#             park = yield self.db.park.find_one({"_id": ObjectId(park_id)})
#             for carpot in park["carports"]:
#                 carport_options[str(carpot['_id'])] = carpot['number']
#         return self.write(json.dumps(carport_options))


# @route(r'/sensors', name='sensors')
# class SensorHandler(RequestHandler):

#     @gen.coroutine
#     def get(self):
#         park_options = []
#         cursor = self.db.park.find()
#         while (yield cursor.fetch_next):
#             park = cursor.next_object()
#             park_options.append((park['_id'], park['name']))
#         return self.render("sensor.html", park_options=park_options)

#     @gen.coroutine
#     def post(self):
#         park_id = self.get_body_argument("park", default="")
#         carport_id = self.get_body_argument("carport", default="")
#         number = self.get_body_argument("number", default="")

@route(r'/appointments', name='appointments')
class AppointmentHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        appointments = []
        return self.render("appointment.html", appointments=appointments);

@route(r'/history', name='history')
class HistoryHandler(RequestHandler):

    @gen.coroutine
    def get(self):
        histories = []
        return self.render("history.html", histories=histories)

@route(r'/members', name='members')
class Members(RequestHandler):

    @gen.coroutine
    def get(self):
        members = []
        return self.render("member.html", members=members)
