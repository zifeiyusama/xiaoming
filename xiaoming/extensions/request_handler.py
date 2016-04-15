#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    xiaoming.extensions.request_handler
    ~~~~~~~~~~~~~~~~~~~~

    override the RequestHandler of tornado, adding flash session and so on

    :copyright: (c) 2016 by 李紫君,杨明晓,侯增起,毕营帅.
"""
import tornado.escape
import tornado.web
from xiaoming.extensions.session import Session, RedisSession
from xiaoming.models import connection

class FlashMessageMixIn(object):
    """
        Store a message between requests which the user needs to see.

        views
        -------

        self.flash("Welcome back, %s" % username, 'success')

        base.html
        ------------

        {% set messages = handler.get_flashed_messages() %}
        {% if messages %}
        <div id="flashed">
            {% for category, msg in messages %}
            <span class="flash-{{ category }}">{{ msg }}</span>
            {% end %}
        </div>
        {% end %}
    """

    def flash(self, message, category='message'):
        messages = self.messages()
        messages.append((categofry, message))
        self.set_secure_cookie('flash_message', tornado.escape.json_encode(messages))

    def messages(self):
        messages = self.get_secure_cookie('flash_message')
        messages = tornado.escape.json_decode(messages) if messages else []
        return messages

    def get_flashed_messages(self):
        messages = self.messages()
        self.clear_cookie('flash_messages')
        return messages


class RequestHandler(tornado.web.RequestHandler, FlashMessageMixIn):
    """ override the tornado RequestHandler and add flash and session"""

    def get_current_user(self):
        user = self.session['user'] if 'user' in self.session else None
        return user

    @property
    def session(self):
        if hasattr(self, '_session'):
            return self._session
        else:
            self.require_setting('permanent_session_lifetime', 'session')
            expires = self.settings['permanent_session_lifetime'] or None
            if 'redis_server' in self.settings and self.settings['redis_server']:
                sessionid = self.get_secure_cookie('sid')
                self._session = RedisSession(self.application.session_store, sessionid, expires_days=expires)
                if not sessionid:
                    self.set_secure_cookie('sid', self._session.id, expires_days=expires)
            else:
                self._session = Session(self.get_secure_cookie, self.set_secure_cookie, expires_days=expires)
            return self._session