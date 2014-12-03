# -*- coding: utf-8 -*-

# Exam number: Y0076998


# The most basic kinds of controller
# - the home page
# - the user log in, log out, register, edit profile pages
# - uploaded images/files


from gluon.tools import Auth

auth = Auth(db)


def index():
    """
    "BootUp will have a home page that shows the 5 most recently created projects and the 5
    projects closest to their funding goal."
    """
    return dict(
        popular = db(db.project.status=='Open for pledges').select(orderby = ~db.project.total_pledged, limitby = (0, 5)), # TODO
        recent = db(db.project.status=='Open for pledges').select(orderby = ~db.project.last_updated, limitby = (0, 5)),
    )


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access 

    ...but we override the built-in web2py form
    """

    # user registration
    if request.args[0] == 'register':
        response.title = 'Sign up'
        response.description = XML('Sign up for an account to fund and create projects.\
            Already signed up? <a href="' + URL('user/login') + '">Go to log in</a>')
        form = SQLFORM.factory(db.auth_user, db.credit_card, db.address)
        if form.process().accepted:
            address_id = db.address.insert(**db.address._filter_fields(form.vars))
            # (for now, assuming that billing address = shipping address)
            form.vars.shipping_address = address_id
            form.vars.billing_address = address_id
            form.vars.credit_card = db.credit_card.insert(**db.credit_card._filter_fields(form.vars))
            db.auth_user.insert(**db.auth_user._filter_fields(form.vars))
            session.flash = 'Your account has been created, you can now log in'
            # try to log in - TODO
            # session.logged_in_user = form.vars.username
            redirect(URL('projects', 'dashboard'))
        elif form.errors:
            response.flash = 'Sorry, your account couldn’t be created – see errors below'
        return dict(form=form)

    # user profile (edit user)
    elif request.args[0] == 'profile':
        form = auth()

        credit_card = db(db.credit_card.id == auth.user.credit_card).select().first()
        credit_card_form = SQLFORM(db.credit_card, record = credit_card, showid = False)
        if credit_card_form.accepts(request, session):
            response.flash = 'Credit card updated'

        address = db(db.address.id == auth.user.shipping_address).select().first()
        address_form = SQLFORM(db.address, record = address, showid = False)
        if address_form.accepts(request, session):
            response.flash = 'Address updated'

        return dict(form = form, credit_card_form = credit_card_form, address_form = address_form)

    # use default web2py things for everything elese
    elif request.args[0] == 'login':
        response.title = 'Log in'
    form = auth()
    return dict(form = form)


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
