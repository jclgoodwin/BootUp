# -*- coding: utf-8 -*-

# Exam number: Y0076998

# More controllers, relating to projects


from datetime import datetime


def search():
    """
    "People interested in pledging should be able to search from any page for projects of
    interest. They should be able to search for words in the title or in the short description.

    "People interested in pledging should be able to search by category of project and receive
    a list of projects back in that category."
    """

    # search for words in title or description:
    if request.vars.search:
        search = request.vars.search
        q = ((db.project.status == 'Open for pledges') | (db.project.status == 'Funded')) & (db.project.title.contains(search) | db.project.short_description.contains(search))
        results = db(q).select()
        response.title = T('%s %%{project} matching ‘', symbols=len(results)) + request.vars.search + '’'
        return dict(results = results)
    
    # search by category of project:
    elif request.vars.category:
        response.title = request.vars.category + ' projects'
        p = db.project
        q = ((db.project.status == 'Open for pledges') | (db.project.status == 'Funded')) & (db.project.category==request.vars.category)
        results = db(q).select()
        return dict(results = results)

    else:
        raise HTTP(404)


def view():
    """
    View a single project.

    "For each project that is Open for Pledges, funders will be able visit a page where they
    can get information about a Bootable. This page should show the funding goal and the
    total pledged progress toward that goal and the pledge/reward options for the project.
    The page should also show the user`s of those who have contributed, what they
    have contributed and what their expected rewards will be.

    "Users can choose to pledge money to a Bootable from a pre-defined set of pledge values
    (referred to by users as “a Booting”) in exchange for a pre-defined set of rewards.
    When users pledge money to the total pledged, their name and pledge level is added to
    the list of pledgers. Further, when users visit pages to which they have already pledged,
    that page should indicate"
    """

    if len(request.args) > 0:
        project = db(((db.project.status == 'Open for pledges') | (db.project.status == 'Funded')) & (db.project.id == request.args[0])).select().render(0, fields = [db.project.manager])
        if project:
            available_pledges = db(db.available_pledge.project == project.id).select(orderby = db.available_pledge.amount),
            pledged_pledges = db(
                (db.available_pledge.project == project.id)
                & (db.pledged_pledge.pledge == db.available_pledge.id)
                & (db.pledged_pledge.pledger == db.auth_user.id)
            ).select(db.auth_user.username, db.available_pledge.amount, db.available_pledge.reward)

            return dict(
                project = project,
                available_pledges = available_pledges,
                pledged_pledges = pledged_pledges,
            )
        raise HTTP(404)


@auth.requires_login()
def edit():
    """
    'Bootable' creation form

    Create a project, managed by the logged-in user.
    """
    response.title = 'New project'
    form = SQLFORM(db.project, submit_button = 'Save draft')

    if form.process().accepted:
        response.flash = 'Project saved'
    elif form.errors:
        response.flash = 'Sorry, your project couldn’t be saved – see errors below'

    return dict(form = form)


@auth.requires_login()
def dashboard():
    """
    There is some overlap here with the old `edit` controller above ~ -
    but this can also list, update, delete... and manage `available_pledge`s
    """
    projects = SQLFORM.smartgrid(db.project,
        linked_tables=['available_pledge'],
        constraints= {'project': db.project.manager == auth.user},
        fields     = (db.project.title, db.project.status, db.available_pledge.amount, db.available_pledge.reward),
        searchable = False,
        sortable   = False,
        paginate   = 200,
        deletable  = lambda p : 'status' not in p or p.status != 'Open for pledges',
        editable   = lambda p : 'status' not in p or p.status == 'Draft',
        details    = False,
        create     = True,
        csv        = False, # hide 'export as [format]' links
        maxtextlength = 200, # stop titles being truncated,
        formargs  = { 'showid': False, 'submit_button': 'Save' },
        links     = [{'header': 'Actions', 'body':
                        (lambda row :
                            A('Open project for pledges', _href=URL('projects', 'change_status/' + str(row.id) + '/open'), _class='button')
                            if 'status' in row and row.status == 'Draft'
                            else (
                                A('Close project to pledges', _href=URL('projects', 'change_status/' + str(row.id) + '/open'), _class='button danger')
                                if 'status' in row and row.status != 'Draft'
                                else '')
                        ),
                    },],
        oncreate  = lambda p : None,
    )
    return dict(projects = projects)


@auth.requires_login()
def change_status():
    """
    Open or close a project:

    /projects/change_status/2/open
    /projects/change_status/2/close
    """
    if len(request.args) >= 2:
        project_id = request.args[0]                # ensure logged in user = manager:
        project = db((db.project.id == project_id) & (db.project.manager == auth.user)).select().first()
        action = request.args[1]
        if action == 'open':
            if project.status == 'Draft':
                if len(db(db.available_pledge.project == project_id).select()) == 0:
                    session.flash = 'Sorry, you must add at least one available pledge before you can open a project for pledges'
                else:
                    project.update_record(status = 'Open for pledges', last_updated = datetime.utcnow())
                    session.flash = 'Your project is now open'
            elif project.status == 'Open for pledges':
                session.flash = 'Project was already open'
            else:
                session.flash = 'Sorry, you can’t reopen a project'
        elif action == 'close':
            if project.status != 'Draft':
                session.flash = 'Project closed'
                project.update_record(status = 'Closed')
        redirect(URL('projects', 'dashboard'))


@auth.requires_login()
def pledge():
    """
    Pledge money to a project:

    /projects/pledge/[available_pledge.id]
    """
    if len(request.args) > 0:
        available_pledge_id = request.args[0]
        db.pledged_pledge.insert(pledger = auth.user.id, pledge = available_pledge_id)

        # recompute total:
        project = db((db.available_pledge.id==available_pledge_id) & (db.available_pledge.project == db.project.id)).select().first().project

        project_id = project.id
        pledged_pledges = db(
            (db.available_pledge.project == project.id)
            & (db.pledged_pledge.pledge == db.available_pledge.id)
        ).select(db.available_pledge.amount)

        total_pledged = 0
        for pledge in pledged_pledges:
            total_pledged += pledge.amount
        project.update_record(total_pledged = total_pledged)

        if total_pledged >= project.funding_goal:
            project.update_record(status = 'Funded')

        # redirect back:
        available_pledge = db(db.available_pledge.id == available_pledge_id).select().first()
        session.flash = 'Thank you for pledging. If {0} reaches its funding goal, you will be charged £{2} and receive {3} '.format(project.title, project.funding_goal, available_pledge.amount, available_pledge.reward) 
        redirect(URL('projects', 'view/' + str(project.id)))
