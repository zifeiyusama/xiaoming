#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.constants
    ~~~~~~~~~~~~~~~~~~~~

    constatns variables for classes and others

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
PARK_STATUS = {
    'PREPARING': '筹备中',
    'DISCARDED': '废弃',
    'USING': '使用中'
}

CARPORT_STATUS = {
    'FREE': '空闲',
    'OCCUPIED': '占用',
    'UNAVAILABlE': '不可用'
}

SENSOR_STATUS = {
    'PREPARING': '筹备中',
    'WORKING': '工作正常',
    'BREAKDOWN': '故障',
    'REPAIRING': '维修中'
}

OAUTH_STATUS = {
    'WECHAT':'微信',
    'QQ': 'QQ',
    'WEIBO': '微博'
}

ORDER_STATUS = {
    'OPEN': '开启',
    'CARIN': '已停车',
    'UNPAID': '未付款',
    'PAID': '已付款',
    'CANCELED': '废弃',
    'EVALUATED': '已评价',
    'OVERDUE': '预约过期',
}

SMS_STATUS = {
    'SUCCEED': '成功',
    'FAILD': '失败'
}
