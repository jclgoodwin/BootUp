# -*- coding: utf-8 -*-

# Exam number: Y0076998

from datetime import datetime

# these models are defined in this file:
# - project (Bootable)
# - available_pledge
# - pledged_pledge (relationship between user and available_pledge)

PROJECT_CATEGORIES = [
    'Art',
    'Comics',
    'Crafts',
    'Fashion',
    'Film',
    'Games',
    'Music',
    'Photography',
    'Technology'
]


db.define_table(
    'project',
    Field('manager',
        db.auth_user,
        default   = auth.user.id if auth.user else None, # default to logged in user (but don't cause an error for non--logged-in users)
        writable  = False,
        represent = lambda id, r: db.auth_user(id).username,
    ),

    # "A project title"
    Field('title',
        'string',
        required = True,
        requires = IS_NOT_EMPTY(),
        label    = 'Project title'
    ),

    Field('status',
        'string',
        requires = IS_IN_SET(('Draft', 'Open for pledges', 'Funded', 'Closed')),
        default  = 'Draft',
        writable = False,
    ),

    # "A short project description (maximum of 120 characters long)"
    Field('short_description',
        'text',
        length   = 120,
        requires = IS_LENGTH(120),
        comment  = '120 characters or fewer, to summarize your project'
    ),

    # "A category for the project chosen from a preset group of categories"
    Field('category',
        'string',
        requires = IS_IN_SET(PROJECT_CATEGORIES, error_message = 'Choose a category')
    ),

    # "A funding goal (in GBPs)"
    Field('funding_goal',
        'integer',
        required = True,
        requires = IS_INT_IN_RANGE(1, None, error_message = 'Should be at least £1'),
        label    = 'Funding goal (£)',
        comment  = 'Your project will be funded when your total pledges reach this amount'
    ),

    # "An image to represent the project.
    # The image should be in JPG, PNG or GIF format.
    # You can assume that the images will be in 4:3 aspect ratio
    # and will be less than 1024 x 768 pixels"
    Field('picture',
        'upload',
        required = True,
        requires = IS_IMAGE(),
        comment  = 'Upload a picture to represent your project'
    ),

    # "A long description of the project goals"
    Field('long_description',
        'text',
        required = True,
        requires = IS_NOT_EMPTY(),
        label    = 'Long description',
        comment  = 'A longer description of your project goals'
    ),

    # "A story about themselves as Bootable Managers and why they want the project funded"
    Field('story',
        'text',
        required = True,
        requires = IS_NOT_EMPTY(),
        comment  = 'A story about you as a Bootable Manager, and why you want the project funded'
    ),
    
    # for the 'latest projects' query
    Field('last_updated',
        'datetime',
        compute = lambda p: datetime.utcnow(),
    ),

    # to simplify the 'popular projects' query
    Field('distance_to_funding',
        'integer',
        readable = False,
        writable = False,
    ),
)


# "A set of possible pledges"
db.define_table(
    'available_pledge',
    Field('amount', 'integer'),
    Field('project', db.project),
    Field('reward', 'string'),
    # format = '%(reward)s',
)


# "A pledge list that lists all people who have pledged funding to the project"
db.define_table(
    'pledged_pledge',
    Field('pledger',
        db.auth_user,
        default = auth.user.id if auth.user else None
    ),
    Field('project', db.project),
    # format = '%(reward)s',
)
