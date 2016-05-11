#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.api
    ~~~~~~~~~~~~~~~~~~~~

    the api for outer application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
from xiaoming.extensions.request_handler import RequestHandler
from xiaoming.extensions.routing import route

from datetime import datetime
from bson.objectid import ObjectId

from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
import tornado.web
import logging
import random
import json
import re


@route(r'/api/parks/([a-z]*)', name='parks_api')
class ParksAPI(RequestHandler):


    def get(self, method):
        if hasattr(self, method):
            getattr(self, method)()
        else:
            return self.set_status(404)

    @tornado.web.asynchronous
    @gen.coroutine
    def all(self):
        result = []
        free_carports = {}
        free_carports_cursor = self.db.carport.find({'status':'FREE'})
        while (yield free_carports_cursor.fetch_next):
            doc = free_carports_cursor.next_object()
            park_id = str(doc['park_id'])
            if park_id in free_carports:
                free_carports[park_id] += 1
            else:
                free_carports[park_id] = 1
        #TODO:search appointment order
        cursor = self.db.park.find({'status':'USING'}).sort([('name', 1)])
        while (yield cursor.fetch_next):
            doc = cursor.next_object()
            park = {
                '_id': str(doc['_id']),
                'description': doc['description'],
                'name': doc['name'],
                'location':  doc['location'],
                'carport_count': doc['carport_count'],
                'available_carport': free_carports[str(doc['_id'])],
            }
            result.append(park)
        data = {"data": result}
        return self.write(str(data))

    @tornado.web.asynchronous
    @gen.coroutine
    def info(self):
        park = self.get_argument('park_id', default='')
        if park == '':
            return self.set_status(404, reason='MISSING PARAMETER "park_id"')
        park_id = ObjectId(park)
        free_carports_number = yield self.db.carport.find({'status':'FREE', 'park_id': park_id}).count()
        doc = yield self.db.park.find_one({'_id':park_id})
        result = {
            '_id': str(doc['_id']),
            'description': doc['description'],
            'name': doc['name'],
            'location':  doc['location'],
            'carport_count': doc['carport_count'],
            'available_carport': free_carports_number,
        }
        return self.write(str(result))

    @tornado.web.asynchronous
    @gen.coroutine
    def recommend(self):
        self.all()


@route(r'/api/orders/([a-z]*)', name='orders_api')
class OrdersAPI(RequestHandler):
    """ 订单数据结构
    {
        car_number:,
        carport_id:,
        park_id:,
        member_id:,
        phone:,
        is_appointment:,
        appointment_date:,
        status:,
        order_date,
        park_date,
        leave_date,
        park_duration,
        total_price,
        paid_date,
        cancel_date,
        evaluation,
        evaluation_content,
        evaluate_date
    }
    """

    def get(self, method='history'):
        if hasattr(self, method):
            getattr(self, method)()
        else:
            return self.set_status(404)

    def post(self, method='appoint'):
        if hasattr(self, method):
            getattr(self, method)()
        else:
            return self.set_status(404)

    @tornado.web.asynchronous
    @gen.coroutine
    def appoint(self):
        member_id = self.get_argument('member_id', default='')
        park_id = self.get_argument('park_id', default='')
        car_number = self.get_argument('car_number', default='')
        phone = self.get_argument('phone', default='')
        if member_id == '' or park_id == '' or car_number == '' or phone == '':
            return self.set_status(404, 'MISSING ARGUMENT')
        order = yield self.db.order.insert({
            'number': 'O' + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + str(random.randint(1, 9)),
            'car_number': car_number,
            'phone': phone,
            'park_id': park_id,
            'member_id': member_id,
            'is_appointment': True,
            'appointment_date': datetime.utcnow(),
            'status': 'OPEN',
            'order_date': datetime.utcnow(),
            'park_date': '',
            'leave_date': '',
            'park_duration': '',
            'total_price': '',
            'paid_date': '',
            'cancel_date': '',
            'evaluation': '',
            'evaluation_content': '',
            'evaluate_date':''
        })
        result = {}
        if order:
            result = {
                'result': '1',
                'order_id': str(order),
                'error_code': '',
                'error_message’': '',
            }
        else:
            result = {
                'result': '0',
                'order_id': '',
                'error_code': '000',
                'error_message’': '',
            }
        self.write(result)

    @tornado.web.asynchronous
    @gen.coroutine
    def pay(self):
        order_id = self.get_argument('order_id', default='')
        if order_id == '':
            return self.set_status(404, 'MISSING ARGUMENT order_id')
        order = yield self.db.order.find_and_modify({
            "_id": ObjectId(order_id)
        },{
            "$set": {
                'status': 'PAID',
                'paid_date': datetime.utcnow(),
            }
        })
        result = {}
        if '_id' in order:
            result = {
                'result': '1',
                'error_code': '',
                'error_message’': '',
            }
        else:
            result = {
                'result': '0',
                'error_code': '000',
                'error_message’': '',
            }
        self.write(result)

    @tornado.web.asynchronous
    @gen.coroutine
    def info(self):
        order_id = self.get_argument('order_id', default='')
        if order_id == '':
             return self.set_status(404, 'MISSING ARGUMENT')
        order = yield self.db.order.find_one({
            "_id": ObjectId(order_id)
        })
        if '_id' not in order:
             return self.set_status(404, 'ORDER NOT FOUND')
        park = yield self.db.park.find_one({
            "_id": ObjectId(order['park_id'])
        })
        member = yield self.db.member.find_one({
            "_id": ObjectId(order['member_id'])
        })
        result = {
            'number':order['number'],
            'park_id':order['park_id'],
            'park_name':park['name'],
            'member_id':order['member_id'],
            'member_name':member['name'],
            'car_number：':order['car_number'],
            'phone':order['phone'],
            'is_appointment':order['is_appointment'],
            'appointment_date':str(order['appointment_date']),
            'status':order['status'],
            'order_date':str(order['order_date']),
            'park_date':str(order['park_date']),
            'leave_date':str(order['leave_date']),
            'park_duration':order['park_duration'],
            'total_price':order['total_price'],
            'paid_date':str(order['paid_date']),
            'cancel_date':str(order['cancel_date']),
            'evaluation':order['evaluation'],
            'evaluation_content':order['evaluation_content'],
            'evaluate_date':str(order['evaluate_date']),
        }
        self.write(result)

    @tornado.web.asynchronous
    @gen.coroutine
    def evaluate(self):
        order_id = self.get_argument('order_id', default='')
        evaluation = self.get_argument('evaluation', default='')
        evaluation_content = self.get_argument('evaluation_content', default='')
        if order_id == '' or evaluation == '' or evaluation_content == '':
            return self.set_status(404, 'MISSING ARGUMENT')
        order = yield self.db.order.find_and_modify({
            "_id": ObjectId(order_id)
        },{
            "$set": {
                'status': 'evaluated',
                'evaluation': evaluation,
                'evaluation_content': evaluation_content,
                'evaluate_date': datetime.utcnow(),
            }
        })
        result = {}
        if '_id' in order:
            result = {
                'result': '1',
                'error_code': '',
                'error_message’': '',
            }
        else:
            result = {
                'result': '0',
                'error_code': '000',
                'error_message’': '',
            }
        self.write(result)

    @tornado.web.asynchronous
    @gen.coroutine
    def history(self):
        member_id = self.get_argument('member_id', default='')
        if member_id == '':
            return self.set_status(404, 'MISSING ARGUMENT member_id')
        member = yield self.db.member.find_one({
            "_id": ObjectId(member_id)
        })
        if '_id' not in member:
            return self.set_status(404, 'MEMBER NOT FOUND')
        park_ids = []
        orders = []
        order_cursor = self.db.order.find({'member_id':member_id}).sort([('number', 1)])
        while (yield order_cursor.fetch_next):
            doc = order_cursor.next_object()
            park_ids.append(ObjectId(doc['park_id']))
            orders.append(doc)
        parks={}
        park_cursor = self.db.park.find({
            "_id": {'$in': park_ids}
        })
        while (yield park_cursor.fetch_next):
            doc = park_cursor.next_object()
            parks[str(doc['_id'])] = doc['name']
        i = 0
        count = len(orders)
        results = {"data":[]}
        while i < count:
            order = orders[i]
            result = {
                'number':order['number'],
                'park_id':order['park_id'],
                'park_name':parks[order['park_id']],
                'member_id':order['member_id'],
                'member_name':member['name'],
                'car_number：':order['car_number'],
                'phone':order['phone'],
                'is_appointment':order['is_appointment'],
                'appointment_date':str(order['appointment_date']),
                'status':order['status'],
                'order_date':str(order['order_date']),
                'park_date':str(order['park_date']),
                'leave_date':str(order['leave_date']),
                'park_duration':order['park_duration'],
                'total_price':order['total_price'],
                'paid_date':str(order['paid_date']),
                'cancel_date':str(order['cancel_date']),
                'evaluation':order['evaluation'],
                'evaluation_content':order['evaluation_content'],
                'evaluate_date':str(order['evaluate_date']),
            }
            results["data"].append(result)
            i += 1
        self.write(results)

    @tornado.web.asynchronous
    @gen.coroutine
    def cancel(self):
        order_id = self.get_argument('order_id', default='')
        if order_id == '':
            return self.set_status(404, 'MISSING ARGUMENT order_id')
        order = yield self.db.order.find_and_modify({
            "_id": ObjectId(order_id)
        },{
            "$set": {
                'status': 'canceled',
                'cancel_date': datetime.utcnow(),
            }
        })
        result = {}
        if '_id' in order:
            result = {
                'result': '1',
                'error_code': '',
                'error_message’': '',
            }
        else:
            result = {
                'result': '0',
                'error_code': '000',
                'error_message’': '',
            }
        self.write(result)


@route(r'/api/members/([a-z]*)', name='members_api')
class MembersAPI(RequestHandler):
    """
    {
        name ,
        phone ,
        password ,
        register_date ,
        level ,
        car_number
    }
    """

    def get(self, method='login'):
        if hasattr(self, method):
            getattr(self, method)()
        else:
            return self.set_status(404)

    @tornado.web.asynchronous
    @gen.coroutine
    def register(self):
        phone = self.get_argument('phone', default='')
        password = self.get_argument('password', default='')
        name = self.get_argument('name', default='')
        if phone == '' or password == '' or name == '':
            return self.set_status(404, 'MISSING ARGUMENT')
        result = {}
        member = yield self.db.member.insert({
            'name': name,
            'phone': phone,
            'password': password,
            'register_date': datetime.utcnow(),
            'level': '',
            'last_login_date':'',
            'car_number':[]
        })
        if member:
            result = {
                'result': '1',
                'member_id': str(member),
                'error_code': '',
                'error_message’': '',
            }
        else:
            result = {
                'result': '0',
                'member_id': '',
                'error_code': '000',
                'error_message’': '注册失败',
            }
        self.write(result)

    @tornado.web.asynchronous
    @gen.coroutine
    def login(self):
        phone = self.get_argument('phone', default='')
        password = self.get_argument('password', default='')
        result = {}
        if phone == '' or password == '':
            return self.set_status(404, 'MISSING ARGUMENT')
        member = yield self.db.member.find_one({'phone': phone, 'password': password})
        if member:
            result['result'] = '1'
            result['member_id'] = str(member['_id'])
            result['error_code'] = ''
            result['error_message'] = ''
        else:
            result['result'] = '0'
            result['member_id'] = ''
            result['error_code'] = '000'
            result['error_message'] = '账号密码不正确'
        self.write(result)

    @tornado.web.asynchronous
    @gen.coroutine
    def info(self):
        member_id = self.get_argument('member_id', default='')
        if member_id == '':
           return self.set_status(404, 'MISSING ARGUMENT')
        result = {}
        member = yield self.db.member.find_one({'_id': ObjectId(member_id)})
        if member:
            result['member_id'] = str(member['_id'])
            result['name'] = member['name']
            result['phone'] = member['phone']
            result['register_date'] = str(member['register_date'])
            result['last_login_date'] =str(member['last_login_date'])
            result['level'] = member['level']
            result['car_number'] = member['car_number']
            self.write(result)
        else:
            return self.set_status(404, 'MEMBER NOT FOUND')

    @tornado.web.asynchronous
    @gen.coroutine
    def modify(self):
        member_id = self.get_argument('member_id', default='')
        name = self.get_argument('name', default='')
        phone = self.get_argument('phone', default='')
        car_number = self.get_argument('car_number', default='')
        password = self.get_argument('password', default='')
        if member_id == '':
            return self.set_status(404, 'MISSING ARGUMENT member_id')
        info = {}
        result = {}
        if name != '':
            info['name'] = name
        if phone != '':
            info['phone'] = phone
        if car_number != '':
            car_number_list = eval(car_number)
            info['car_number'] = car_number_list
        if password != '':
            info['password'] = password
        member = yield self.db.member.find_and_modify({
            "_id": ObjectId(member_id)
        },{
            "$set": info
        })
        if member:
            result = {
                'result': '1',
                'error_code': '',
                'error_message': '',
            }
        else:
            result = {
                'result': '0',
                'error_code': '',
                'error_message': '',
            }
        self.write(result)


@route(r'/api/sms/([a-z]*)', name='sms_api')
class SMSAPI(RequestHandler):

    def get(self, method):
        if hasattr(self, method):
            getattr(self, method)()
        else:
            return self.set_status(404)

    @tornado.web.asynchronous
    @gen.coroutine
    def captcha(self):
        mobile = self.get_argument('mobile', default='')
        if mobile == '':
            return self.set_status(404, 'MISSING ARGUMENT mobile')
        if not re.match(r'^0?(13|14|15|18|17)[0-9]{9}$', mobile):
            return self.set_status(404, 'INVALID MOBILE NUMBER')
        code = ''
        for x in range(6):
            code = code + str(random.randint(0, 9))
        content = '【小明停车场】您的登录验证码是' + code + '，有效时间5分钟，请不要告诉他人！'
        query_param = body='mobile=' + mobile + '&content=' + content + '&tag=2'
        request = HTTPRequest('http://apis.baidu.com/kingtto_media/106sms/106sms?' + query_param,
            headers={'apikey':'baf36226755e86a49d4201e28c77590b'},
        )
        client = AsyncHTTPClient()
        response = yield client.fetch(request)
        result = json.loads(response.body.decode())
        result['captcha'] = code
        return self.write(result)
