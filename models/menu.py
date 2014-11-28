# -*- coding: utf-8 -*-

# Exam number: Y0076998

from gluon.tools import Auth

auth = Auth(db)

if auth.is_logged_in():
    response.user_menu = [
        (T('Dashboard'), False, URL('default', 'dashboard')),
        (T('New project'), False, URL('projects', 'create')),
        (T('Profile'), False, URL('default', 'user/profile')),
        (T('Log out'), False, URL('default', 'user/logout')),
    ]
else:
    response.user_menu = [
        (T('Sign up'), False, URL('default', 'user/register')),
        (T('Log in'),  False, URL('default', 'user/login')),
    ]
