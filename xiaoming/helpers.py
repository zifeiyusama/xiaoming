#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.helpers
    ~~~~~~~~~~~~~~~~~~~~

    the helper class and function of xiaoming application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
from datetime import datetime
import random


def setting_from_object(obj):
    settings = dict()
    for key in dir(obj):
        if key.isupper():
            settings[key.lower()] = getattr(obj, key)
    return settings

def init_insert(namespace=None, user_id=None):
    result = {}
    if namespace is not None:
        result['number'] = namespace + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + str(random.randint(1, 9))
    result['created_date'] = datetime.utcnow()
    result['created_by'] = user_id
    result['last_modified_date'] = datetime.utcnow()
    result['last_modified_by'] = user_id
    return result

def init_update(namespace=None, user_id=None):
    result = {}
    result['last_modified_date'] = datetime.utcnow()
    result['last_modified_by'] = user_id
    return result
