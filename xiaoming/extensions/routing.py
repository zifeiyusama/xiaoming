#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.extensions.routing
    ~~~~~~~~~~~~~~~~~~~~

    add routing decorator like Flask to tornado

    Example:
    @route(r'/', name='index')
    class IndexHandler(tornado.web.RequestHandler):
        pass

    class Application(tornado.web.Application):
        def __init__(self):
            handlers = [
                # ...
            ] + Route.routes()

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
from tornado.web import url
from functools import reduce

class Route(object):

    _routes = {}

    def __init__(self, pattern, kwargs={}, name=None, host='.*$'):
        self.pattern = pattern
        self.kwargs = kwargs
        self.name = name
        self.host = host

    def __call__(self, handler_class):
        spec = url(self.pattern, handler_class, self.kwargs, name=self.name)
        self._routes.setdefault(self.host, []).append(spec)
        return handler_class

    @classmethod
    def routes(cls, application=None):
        if application:
            for host, handlers in cls._routes.items():
                application.add_handlers(host, handlers)
        else:
            return reduce(lambda x,y:x+y, cls._routes.values()) if cls._routes else []

    @classmethod
    def url_for(cls, name, *args):
        named_handlers = dict([(spec.name, spec) for spec in cls.routes() if spec.name])
        if name in named_handlers:
            return named_handlers[name].reverse(*args)
        raise KeyError("%s not found in named urls" % name)

route = Route