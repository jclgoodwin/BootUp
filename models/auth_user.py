# -*- coding: utf-8 -*-

from gluon.tools import Auth

db = DAL("sqlite://storage.sqlite")

auth = Auth(db)

auth.settings.extra_fields['auth_user'] = [
    Field('birth_date',
        'date',
        required = True,
        label = 'Date of birth',
        requires = [IS_NOT_EMPTY(), IS_DATE(error_message = 'Should be in the form YYYY-MM-DD')]
        ),
    Field('credit_card_number',
        'integer',
        length = 16,
        required = True,
        label = 'Credit card number',
        requires=[IS_NOT_EMPTY(), IS_LENGTH(16, 16, error_message = 'Should be 16 digits')]
        ),
    ]

auth.define_tables(username = True, signature = False)

auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

db.auth_user.email.readable = db.auth_user.email.writable = False 

auth.default_messages['login_button'] = 'Log in' # verb
auth.default_messages['register_button'] = 'Sign up'
