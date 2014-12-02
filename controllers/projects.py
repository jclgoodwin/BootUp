# -*- coding: utf-8 -*-

# Exam number: Y0076998


# More controllers, relating to projects


def search():
    """
    People interested in pledging should be able to search from any page for projects of
    interest. They should be able to search for words in the title or in the short description.

    People interested in pledging should be able to search by category of project and receive
    a list of projects back in that category.
    """

    # search for words in title or description
    if request.vars.search:
        search = request.vars.search
        q = (db.project.status=='Open for pledges') & (db.project.title.contains(search) | db.project.short_description.contains(search))
        results = db(q).select()
        response.title = T('%s %%{project} matching ‘', symbols=len(results)) + request.vars.search + '’'
        return dict(results = results)
    
    # search by category of project
    elif request.vars.category:
        response.title = request.vars.category + ' projects'
        p = db.project
        q = (db.project.status=='Open for pledges') & (db.project.category==request.vars.category)
        results = db(q).select()
        return dict(results = results)

    else:
        raise HTTP(404)


def view():
    """
    View a single project.

    For each project that is Open for Pledges, funders will be able visit a page where they
    can get information about a Bootable. This page should show the funding goal and the
    total pledged progress toward that goal and the pledge/reward options for the project.
    The page should also show the user`s of those who have contributed, what they
    have contributed and what their expected rewards will be.

    Users can choose to pledge money to a Bootable from a pre-defined set of pledge values
    (referred to by users as “a Booting”) in exchange for a pre-defined set of rewards.
    When users pledge money to the total pledged, their name and pledge level is added to
    the list of pledgers. Further, when users visit pages to which they have already pledged,
    that page should indicate
    """
    if len(request.args) > 0:
        project = db((db.project.status=='Open for pledges') & (db.project.id==request.args[0])).select().render(0, fields=[db.project.manager])
        if project:
            return dict(
                project = project,
                available_pledges = db(db.available_pledge.project == project.id).select(),
                pledged_pledges   = db(db.pledged_pledge.project == project.id).select(),
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
    There is some overlap here with the `edit` controller - it allows creating new Bootables -
    but this can also list, edit, delete...
    """
    projects = SQLFORM.grid(db.project.manager == auth.user.id,
        fields     = (db.project.title, db.project.status),
        searchable = False,
        sortable   = False,
        paginate   = 200,
        deletable  = lambda p : p.status != 'Open for pledges',
        editable   = lambda p : p.status == 'Draft',
        details    = False,
        create     = True,
        csv        = False, # hide 'export as [format]' links
        maxtextlength = 200, # stop titles being truncated,
        formargs = { 'showid': False, 'submit_button': 'Save draft' },
    )
    return dict(projects = projects)


@auth.requires_login()
def manage_pledges():
    """
    Create, edit, delete `available_pledge`s for projects managed by the logged-in user.
    """
    if request.args[0]:
        grid = SQLFORM.grid(db.available_pledge.project == 3,
            fields     = (db.available_pledge.reward),
            searchable = False,
            sortable   = False,
            paginate   = 200,
            details    = False,
            create     = True,
            csv        = False, # hide 'export as [format]' links
            maxtextlength = 200, # stop titles being truncated,
            formargs = { 'showid': False, 'submit_button': 'Save pledge' },
        )
        return dict(grid = grid)
    raise HTTP(404)


