# -*- coding: utf-8 -*-

# Exam number: Y0076998

# Here we make use of web2py's built-in user models,
# but add some extra fields to meet our requirements.
#
# These models are defined in this file:
# - address
# - credit_card
# - auth_user (based on the built-in web2py one)

from gluon.tools import Auth

db = DAL("sqlite://storage.sqlite")

auth = Auth(db)

db.define_table(
    'address',
    Field('street',   
        'string',
        required = True,
        requires = IS_NOT_EMPTY(),
        label = 'Street address',
    ),
    Field('city',     
        'string',
        required = True,
        requires = IS_NOT_EMPTY(),
    ),
    Field('postcode', 
        'string',
        required = True,
        requires = IS_NOT_EMPTY(),
    ),
    Field('country',  
        'string',
        required = True,
        requires = IS_NOT_EMPTY(),
    ),
)

db.define_table(
    'credit_card',
    Field('number',
        'integer',
        length    = 16,
        required  = True,
        requires  = [IS_NOT_EMPTY(), IS_LENGTH(16, 16)],
        label     = 'Credit card number',
    ),
    Field('expiry_date',
        'string', # dubious way to avoid the web2py date picker (which does not recognise the YYYY-MM format)
        required = True,
        requires = [IS_NOT_EMPTY(), IS_DATE(format=T('%Y-%m'), error_message = 'Should be in the form YYYY-MM')],
        label    = 'Expiry date',
        comment  = 'In the format YYYY-MM',
    ),
    Field('security_code',
        'integer',
        length   = 3,
        required = True,
        requires = [IS_NOT_EMPTY(), IS_LENGTH(3, 3, error_message = 'Should be 3 digits')],
        label    = 'Security code',
        comment  = 'The 3-digit number on the back of your card',
    ),
    Field('billing_address',
        'reference address',
        writable  = False,
        readable  = False,
    ),
)

auth.settings.extra_fields['auth_user'] = [
    Field('birth_date',
        'date',
        required = True,
        label    = 'Date of birth',
        comment  = 'In the format YYYY-MM-DD',
        requires = [IS_NOT_EMPTY(), IS_DATE(error_message = 'Should be in the form YYYY-MM-DD')]
    ),
    Field('real_name',
        'string',
        required = True,
        label    = 'Real name',
        requires = IS_NOT_EMPTY()
    ),
    Field('credit_card',
        'reference credit_card',
        writable  = False,
        readable  = False,
        represent = lambda id, r: db.credit_card(id).number,
    ),
    Field('shipping_address',
        'reference address',
        writable = False,
        readable = False,
    ),
]

auth.define_tables(username = True, signature = False)

# hide some default web2py fields
db.auth_user.email.readable = db.auth_user.email.writable = False
db.auth_user.first_name.readable = db.auth_user.first_name.writable = False
db.auth_user.last_name.readable = db.auth_user.last_name.writable = False

# change various auth/login settings

auth.settings.registration_requires_verification   = False
auth.settings.registration_requires_approval       = False
auth.settings.reset_password_requires_verification = True

auth.default_messages['login_button']    = 'Log in'
auth.default_messages['register_button'] = 'Sign up'
