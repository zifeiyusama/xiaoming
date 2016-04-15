#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming
    ~~~~~~~~~~~~~~~~~~~~

    models for xiaoming Application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
from mongokit import Document, Connection
from datetime import datetime
from pymongo.objectid import ObjectId
from settings import MONGO_HOST, MONGO_PORT

connection = Connection(host=MONGO_HOST, port=MONGO_PORT)


@connection.register
class Park(Document):
    # TODO: 停车场位置信息
    __database__ = 'park'
    __collection__ = 'park'
    structure = {
        'number': basestring,
        'description': basestring,
        'carport_count': int,
        'status': IS('筹备中', '使用中', '废弃'),
        'created_by': ObjectId,
        'created_date': datetime,
        'last_modified_by': ObjectId,
        'last_modified_date': datetime
    }
    required_fields = ['number']
    default_values = {
        'status': '筹备中',
        'carport_count': 0,
        'created_date': datetime.utcnow,
        'last_modified_date': datetime.utcnow
    }


@connection.register
class Carport(Document):
    __database__ = 'park'
    __collection__ = 'carport'
    structure = {
        'number': basestring,
        'status': IS('空闲', '预约', '占用', '不可用'),
        'sensors': list,
        'position': dict,
        'park': ObjectId,
        'created_by': ObjectId,
        'created_date': datetime,
        'last_modified_by': ObjectId,
        'last_modified_date': datetime
    }
    required_fields = ['number']
    default_values = {
        'status': '不可用',
        'created_date': datetime.utcnow,
        'last_modified_date': datetime.utcnow
    }


@connection.register
class Sensor(Document):
    __database__ = 'park'
    __collection__ = 'sensor'
    structure = {
        'number': basestring,
        'status': IS('工作正常', '故障', '维修中', '筹备中'),
        'carport': ObjectId,
        'created_by': ObjectId,
        'created_date': datetime,
        'last_modified_by': ObjectId,
        'last_modified_date': datetime
    }
    required_fields = ['number', 'carport']
    default_values = {
        'status': '筹备中',
        'created_date': datetime.utcnow,
        'last_modified_date': datetime.utcnow
    }


@connection.register
class Member(Document):
    __database__ = 'park'
    __collection__ = 'member'
    structure = {
        'number': basestring,
        'name': basestring,
        'phone': basestring,
        'password':basestring,
        'register_date': datetime,
        'level': basestring,
    }
    required_fields = ['number', 'name', 'phone', 'password', 'register_date']
    default_values = {
        'register_date': datetime.utcnow,
    }


@connection.register
class OAuth(Document):
    __database__ = 'park'
    __collection__ = 'oauth'
    structure = {
        'member_id': ObjectId,
        'oauth_name': IS('weichat', 'qq', 'weibo'),
        'oauth_id': basestring,
        'access_token': basestring,
        'oauth_expires': basestring,
    }


@connection.register
class Order(Document):
    __database__ = 'park'
    __collection__ = 'order'
    structure = {
        'number':basestring,
        'car_number':basestring,
        'carport': ObjectId,
        'member': ObjectId,
        'order_date': datetime,
        'type': IS('预约', '非预约'),
        'status': IS('开启', '已停车', '未付款', '已付款', '废弃'),
        'appointment_date': datetime,
        'park_date': datetime,
        'leave_date': datetime,
        'park_duration': datetime,
        'total_price':float,
        'payment': ObjectId,
        'paid_date': datetime,
        'cancel_date': datetime,
        'paid_date': datetime,
        'created_by': ObjectId,
        'created_date': datetime,
        'last_modified_by': ObjectId,
        'last_modified_date': datetime
    }
    required_fields = ['number', 'carport', 'member', 'type', 'status']
    default_values = {
        'type' '非预约'
        'status': '已停车',
        'created_date': datetime.utcnow,
        'last_modified_date': datetime.utcnow
    }


@connection.register
class  SMS(Document):
    __database__ = 'park'
    __collection__ = 'sms'
    structure = {
        'number': basestring,
        'from': basestring,
        'to': basestring,
        'theme': basestring,
        'content': basestring,
        'sent_date': datetime,
        'parent': ObjectId,
        'status': IS('成功', '失败'),
        'failed_reason': basestring
    }
    required_fields = ['number', 'from', 'to', 'theme', 'content', 'sent_date', 'parent', 'status']
    default_values = {
        'status': '成功'
    }
@connection.register
class  Admin(Document):
    __database__ = 'park'
    __collection__ = 'admin'
    structure = {
        'email': basestring,
        'name': basestring,
        'password': basestring,
        'created_date': datetime,
    }
    required_fields = ['email', 'name', 'password', 'created_date']
