# -*- coding: utf-8 -*-

# Exam number: Y0076998

PROJECT_STATUSES = (
    'Draft',
    'Open for pledges',
    'Funded',
    'Not funded'
)

PROJECT_CATEGORIES = (
    'Art',
    'Comics',
    'Crafts',
    'Fashion',
    'Film',
    'Games',
    'Music',
    'Photog raphy',
    'Technology'
)

if auth.user:
    logged_in_user_id = auth.user.id
else:
    logged_in_user_id = None

db.define_table(
    'project',
    Field('manager', db.auth_user, default=logged_in_user_id, writable=False),

    # A project title
    Field('title', required=True, label='Project title'),

    Field('status', 'text', requires=IS_IN_SET(PROJECT_STATUSES), default='Draft', writable=False),

    # A short project description (maximum of 120 characters long)
    Field('short_description', 'text', length=120, comment='120 characters or fewer, to summarize your project'),

    # A category for the project chosen from a preset group of categories
    Field('category', 'string', requires=IS_IN_SET(PROJECT_CATEGORIES)),

    # A funding goal (in GBPs)
    Field('funding_goal', 'integer', label='Funding goal (£)', comment='Your project will be funded when your total pledges reach this amount'),

    # An image to represent the project.
    # The image should be in JPG, PNG or GIF format.
    # You can assume that the images will be in 4:3 aspect ratio and will be less than 1024 x 768 pixels
    Field('picture', 'upload', requires=IS_IMAGE(), comment='Upload a picture to represent your project'),

    # A long description of the project goals
    Field('long_description', 'text', comment='A longer description of your project goals'),

    # A story about themselves as Bootable Managers and why they want the project funded
    Field('story', 'text', comment='A story about you as a Bootable Manager, and why you want the project funded'),
    
    format = '%(name)s'
)

# A set of possible pledges
db.define_table(
    'available_pledge',
    Field('amount',  'integer'),
    Field('project', db.project),
    Field('reward',  'string'),
)

# A pledge list that lists all people who have pledged funding to the project 
db.define_table(
    'pledged_pledge',
    Field('pledger', db.auth_user),
    Field('project', db.project)
)
