# -*- coding: utf-8 -*-

from gluon.tools import Auth

db = DAL("sqlite://storage.sqlite")

auth = Auth(db)

auth.define_tables(username=True, signature=False)

auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

db.auth_user.first_name.readable = db.auth_user.first_name.writable = False 
db.auth_user.last_name.readable = db.auth_user.last_name.writable = False 
db.auth_user.email.readable = db.auth_user.email.writable = False 

auth.settings.extra_fields['auth_user'] = [
    Field('birth_date', 'date')
]
