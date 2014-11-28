# -*- coding: utf-8 -*-

# Exam number: Y0076998

def index():
    """
    Home Page:

    BootUp will have a home page that shows the 5 most recently created projects and the 5
    projects closest to their funding goal.
    
    """
    return dict(
        popular = db(db.project).select(),
        recent = db(db.project).select()
        )

@auth.requires_login()
def dashboard():
    return dict(projects=db(db.project.manager == auth.user).select())

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
    # if request.args[0] == 'register':
    #     form = SQLFORM.factory(db.auth_user, db.credit_card, db.address)
        
    #     if form.accepts(request, session):
    #         response.flash = XML('Registation successful. <a href="' + URL('user/login') + '">Log in?</a>')

    #     my_extra_element = LABEL(
    #         'I agree to the terms and conditions',
    #         INPUT(_name='agree', _type='checkbox')
    #         )
    #     form[0].insert(-1,my_extra_element)

    #     db.credit_card.number.show_if = (db.auth_user.username==True)
    
    if request.args[0] == 'login':
        response.title = 'Log in'
    elif request.args[0] == 'register':
        response.title = 'Sign up'
        response.description = XML('Sign up for an account to fund and create projects. Already signed up? <a href="' + URL('user/login') + '">Go to log in</a>')

    form = auth()
    
    return dict(form=form)

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)
