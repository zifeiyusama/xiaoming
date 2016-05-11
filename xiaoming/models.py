#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.models
    ~~~~~~~~~~~~~~~~~~~~

    models for xiaoming Application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
from datetime import datetime

from mongoengine import connect, Document
from mongoengine.fields import (StringField, DateTimeField, ObjectIdField, ReferenceField,
                                IntField, EmailField, DictField,EmbeddedDocumentField, EmbeddedDocument,
                                ListField, FloatField, BooleanField)

from xiaoming.settings import MONGO_HOST, MONGO_PORT, MONGO_DATABASE
from xiaoming.constants import PARK_STATUS, CARPORT_STATUS, SENSOR_STATUS, OAUTH_STATUS, ORDER_STATUS, SMS_STATUS

connect(MONGO_DATABASE, host=MONGO_HOST, port=MONGO_PORT)


class Admin(Document):
    email = EmailField(required=True)
    name = StringField(required=True)
    password = StringField(required=True)
    created_date = DateTimeField(required=True)


class BaseDocument(Document):
    number = StringField(required=True)
    created_by = ReferenceField(Admin)
    created_date = DateTimeField(required=True)
    last_modified_by = ReferenceField(Admin)
    last_modified_date = DateTimeField()

    meta = {'allow_inheritance': True}

    def prepare_save():
        if self.created_date is None:
            self.created_date = datetime.utcnow()
        self.last_modified_date = datetime.utcnow()


class BaseEmbeddedDocument(EmbeddedDocument):
    number = StringField(required=True)
    created_by = ReferenceField(Admin)
    created_date = DateTimeField(required=True)
    last_modified_by = ReferenceField(Admin)
    last_modified_date = DateTimeField()

    meta = {'allow_inheritance': True}

    def prepare_save():
        if self.created_date is None:
            self.created_date = datetime.utcnow()
        self.last_modified_date = datetime.utcnow()


class Carport(BaseEmbeddedDocument):
    # todo 测试内嵌文档是否有id
    status = StringField(choices=CARPORT_STATUS)
    position = DictField()
    sensor_status = StringField(choices=SENSOR_STATUS)


class Park(BaseDocument):
    description = StringFieeld()
    address = StringFieeld()
    carport_count = IntField(default=0)
    carports = ListField(EmbeddedDocumentField(Carport))
    status = StringField(choices=PARK_STATUS)

class Oauth(EmbeddedDocument):
    oauth_name = StringField(choices=OAUTH_STATUS, required=True)
    oauth_id = StringField(required=True)
    access_token = StringField(required=True)
    oauth_expires = FloatField(required=True)


class Member(BaseDocument):
    name = StringField(required=True)
    phone = StringField(required=True)
    password = StringField(required=True)
    register_date = DateTimeField(required=True)
    level = StringField()
    oauth = ListField(EmbeddedDocumentField(Oauth))


class Order(BaseDocument):
    car_number = StringField(required=True)
    carport = StringField(required=True)
    park = ReferenceField(Park, required=True)
    member = ReferenceField(Member)
    is_appointment = BooleanField()
    appointment_date = DateTimeField()
    status = StringField(choices=ORDER_STATUS)
    order_date = DateTimeField()
    park_date = DateTimeField()
    leave_date = DateTimeField()
    park_duration = StringField()
    total_price = FloatField()
    paid_date = DateTimeField()
    cancel_date = DateTimeField()


class SMS(BaseDocument):
    sender = StringField(required=True)
    receiver = StringField(required=True)
    theme = StringField(required=True)
    content = StringField(required=True)
    sent_date = StringField(required=True)
    status = StringField(choices=SMS_STATUS, required=True)
    parentid = ObjectIdField(required=True)