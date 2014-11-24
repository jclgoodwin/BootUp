# -*- coding: utf-8 -*-

# Exam number: Y0076998

def search():
    """
    People interested in pledging should be able to search from any page for projects of
    interest. They should be able to search for words in the title or in the short description.
    """
    if request.vars.search:
        results = db(db.project.title.contains(request.vars.search) | db.project.short_description.contains(request.vars.search)).select()
        return dict(results = results)
    else:
        raise HTTP(404)
 
#    People interested in pledging should be able to search by category of project and receive
#    a list of projects back in that category.


def project():
    """
    For each project that is Open for Pledges, funders will be able visit a page where they
    can get information about a Bootable. This page should show the funding goal and the
    total pledged progress toward that goal and the pledge/reward options for the project.
    The page should also show the usernames of those who have contributed, what they
    have contributed and what their expected rewards will be.
    Users can choose to pledge money to a Bootable from a pre-defined set of pledge values
    (referred to by users as “a Booting”) in exchange for a pre-defined set of rewards.
    When users pledge money to the total pledged, their name and pledge level is added to
    the list of pledgers. Further, when users visit pages to which they have already pledged,
    that page should indicate
    """
    if request.args[0]:
        project = db(db.project.id == request.args[0]).select().first()
        if project:
            return dict(
                project          =project,
                available_pledges=db(db.available_pledge.project == project.id).select()
                )
        else:
            raise HTTP(404)
    else:
        raise HTTP(404)

@auth.requires_login()
def create():
    form = SQLFORM(db.project)
    return dict(
        form = form
        )
