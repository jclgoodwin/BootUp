# -*- coding: utf-8 -*-

# Exam number: Y0076998

from gluon.tools import Auth

db = DAL("sqlite://storage.sqlite")

auth = Auth(db)

db.define_table(
    'address',
    Field('street',   'string', required = True),
    Field('city',     'string', required = True),
    Field('postcode', 'string', required = True),
    Field('country',  'string', required = True),
    )

db.define_table(
    'credit_card',
    Field('billing_address', db.address),
    Field('number',
        'integer',
        length    = 16,
        required  = True,
        requires  = [IS_NOT_EMPTY(), IS_LENGTH(16, 16, error_message = 'Should be 16 digits')],
        label     = 'Credit card number',
        represent = lambda s,r: s.number,
        ),
    Field('expiry_date',
        'date',
        required = True,
        requires = [IS_NOT_EMPTY(), IS_DATE(error_message = 'Should be in the form YYYY-MM-DD')],
        label    = 'Expiry date',
        ),
    Field('security_code',
        'integer',
        length   = 3,
        required = True,
        requires = [IS_NOT_EMPTY(), IS_DATE(error_message = 'Should 3 digits')],
        label    = 'Security code',
        comment  = 'The 3-digit number on the back of your card',
        ),
    )

auth.settings.extra_fields['auth_user'] = [
    Field('birth_date',
        'date',
        required = True,
        label    = 'Date of birth',
        requires = [IS_NOT_EMPTY(), IS_DATE(error_message = 'Should be in the form YYYY-MM-DD')]
        ),
    Field('credit_card',      db.credit_card, writable=False, readable=False, represent=lambda id, r: db.credit_card(id).number),
    Field('shipping_address', db.address,     writable=False, readable=False, ),
    ]

auth.define_tables(username = True, signature = False)

auth.settings.registration_requires_verification   = False
auth.settings.registration_requires_approval       = False
auth.settings.reset_password_requires_verification = True

db.auth_user.email.readable = db.auth_user.email.writable = False 

auth.default_messages['login_button']    = 'Log in'
auth.default_messages['register_button'] = 'Sign up'
