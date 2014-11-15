# -*- coding: utf-8 -*-

from gluon.tools import Auth

auth = Auth(db)

if auth.is_logged_in():
    response.user_menu = [
        (T('Dashboard'), False, URL('default', 'dashboard')),
        (T('Log out'), False, URL('default', 'user/logout')),
    ]
else:
    response.user_menu = [
        (T('Sign up'), False, URL('default', 'user/register')),
        (T('Log in'), False, URL('default', 'user/login')),
    ]
