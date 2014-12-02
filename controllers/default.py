# -*- coding: utf-8 -*-

# Exam number: Y0076998

# The most basic kinds of controller

from gluon.tools import Auth

auth = Auth(db)

print auth

def index():
    """
    "BootUp will have a home page that shows the 5 most recently created projects and the 5
    projects closest to their funding goal."

    Provides the view (/views/)
    """
    return dict(
        popular = db(db.project).select(),
        recent = db(db.project.status=='Open for pledges').select(orderby = db.project.last_updated, limitby = (0, 5)),
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

    ...but we override the built-in web2py form for user registration
    """

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
            session.flash = 'Your account has been created'
            # try to log in
            session.logged_in_user = form.vars.username
            redirect(URL('projects', 'dashboard'))
        elif form.errors:
            response.flash = 'Sorry, your account couldn’t be created – see errors below'
        return dict(form=form)

    # elif request.args[0] == 'profile' and auth.user:
        # credit_card = db(db.credit_card.id == auth.user.credit_card).select()
        # print credit_card
        billing = SQLFORM.factory(db.credit_card, record = db(db.credit_card.id == 1).select())
        # if form.accepts(request, session):
            # resonse.flash = 'updated'
        form = auth()
        return dict(form = form, billing = billing)

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
