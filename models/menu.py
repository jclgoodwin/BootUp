# -*- coding: utf-8 -*-

# Exam number: Y0076998


# This is the menu on the top right of every page. It changes depending on whether a user is logged in


from gluon.tools import Auth

auth = Auth(db)

if auth.is_logged_in():
    response.user_menu = [
        (T('Dashboard'), False, URL('projects', 'dashboard')),
        (T('Create new project'), False, URL('projects', 'edit')),
        (T('Profile'), False, URL('default', 'user/profile', vars={'_next': URL('projects', 'dashboard')})),
        (T('Log out'), False, URL('default', 'user/logout')),
    ]
else:
    response.user_menu = [
        (T('Sign up'), False, URL('default', 'user/register')),
        (T('Log in'),  False, URL('default', 'user/login', vars={'_next': URL('projects', 'dashboard')})),
    ]
