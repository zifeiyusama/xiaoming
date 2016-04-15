#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.helpers
    ~~~~~~~~~~~~~~~~~~~~

    the helper class and function of xiaoming application

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""

def setting_from_object(obj):
    settings = dict()
    for key in dir(obj):
        if key.isupper():
            settings[key.lower()] = getattr(obj, key)
    return settings