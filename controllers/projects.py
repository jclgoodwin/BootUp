# -*- coding: utf-8 -*-

def index():
    return dict(
        popular = db(db.project).select(),
        recent = db(db.project).select()
        )

def search():
	if request.vars.search:
		results = db(db.project.title.contains(request.vars.search) | db.project.short_description.contains(request.vars.search)).select()
		return dict(results=results)
	else:
		raise HTTP(404)

def project():
	if request.args[0]:
		project = db(db.project.id == request.args[0]).select().first()
		if project:
			return dict(project=project)
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
	