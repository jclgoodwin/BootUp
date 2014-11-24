# -*- coding: utf-8 -*-

db.define_table(
    'project',
    Field('manager', db.auth_user),
    # A project title
    Field('title'),
    Field('status', 'text', requires=IS_IN_SET(('Draft', 'Open for pledges', 'Funded', 'Not funded'))),
    # A short project description (maximum of 120 characters long)
    Field('short_description', 'text', length=120),
    # A category for the project chosen from a preset group of categories
    Field('category', 'string', requires=IS_IN_SET(('Art', 'Comics', 'Crafts', 'Fashion', 'Film', 'Games', 'Music', 'Photography', 'Technology'))),
    # A funding goal (in GBPs)
    Field('funding_goal', 'integer', label='Funding goal (£)'),
    # An image to represent the project.
    # The image should be in JPG, PNG or GIF format.
    # You can assume that the images will be in 4:3 aspect ratio and will be less than 1024 x 768 pixels
    Field('picture', 'upload', requires=IS_IMAGE()),
    # A long description of the project goals
    Field('long_description', 'text'),
    # A story about themselves as Bootable Managers and why they want the project funded
    Field('story', 'text'),
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
