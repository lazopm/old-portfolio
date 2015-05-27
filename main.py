import os
import urllib

import jinja2
import webapp2
from google.appengine.ext import ndb
from google.appengine.api import mail
from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

ADMIN_GMAIL = "lazopm@gmail.com"

#models
class Image(ndb.Model):
    name = ndb.StringProperty()
    image = ndb.BlobProperty()

class Project(ndb.Model):
    title = ndb.StringProperty()
    tags = ndb.StringProperty(repeated=True)
    cover = ndb.BlobProperty()
    description = ndb.StringProperty()
    full_description = ndb.TextProperty()

class MsgLog(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()
    msg = ndb.StringProperty()
    ip = ndb.StringProperty()
    timestamp = ndb.DateProperty(auto_now_add=True)

#index page
class Main(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

#porfolio page
class Portfolio(webapp2.RequestHandler):
    def get(self):
        projects_query = Project.query()
        projects = projects_query.fetch()
        template_values = {
            'projects': projects
        }
        template = JINJA_ENVIRONMENT.get_template('portfolio.html')
        self.response.write(template.render(template_values))

#new project
class NewProject(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if user.email()==ADMIN_GMAIL:
                template = JINJA_ENVIRONMENT.get_template('new.html')
                self.response.write(template.render())
            else:
                self.error(401)
        else:
            self.redirect(users.create_login_url(self.request.uri))
    def post(self):
        user = users.get_current_user()
        if user:
            if user.email()==ADMIN_GMAIL:
                project = Project(title = self.request.get("title"),
                                  tags = self.request.get_all("tag"),
                                  cover = self.request.get("img"),
                                  description = self.request.get("desc"))
                project_key = project.put()
                self.redirect("/features?key="+str(project_key))
            else:
                self.error(401)
        else:
            self.redirect(users.create_login_url(self.request.uri))

#project editing
class EditProject(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            if user.email()==ADMIN_GMAIL:
                if self.request.get("project"):
                    project = Project.get_by_id(int(self.request.get('project')))
                    project_key = ndb.Key('Project', int(self.request.get('project')))
                    images = Image.query(ancestor = project_key ).fetch()
                    template_values = {
                        'project': project,
                        'images': images
                    }
                else:
                    projects_query = Project.query()
                    projects = projects_query.fetch()
                    template_values = {
                        'projects': projects
                    }
                template = JINJA_ENVIRONMENT.get_template('edit.html')
                self.response.write(template.render(template_values))
            else:
                self.error(401)
        else:
            self.redirect(users.create_login_url(self.request.uri))

    def post(self):
        user = users.get_current_user()
        if user:
            if user.email()==ADMIN_GMAIL:
                project = Project.get_by_id(int(self.request.get('project')))
                project.title = self.request.get("title")
                project.tags = self.request.get_all("tag")
                project.description = self.request.get("desc")
                project.full_description = self.request.get("fulldesc")
                project.put()
                self.redirect("/edit?project="+str(self.request.get('project')))
            else:
                self.error(401)
        else:
            self.redirect(users.create_login_url(self.request.uri))

#message handler
class Message(webapp2.RequestHandler):
    def post(self):
        log = MsgLog(name = self.request.get('name'),
                  email = self.request.get('email'),
                  msg = self.request.get('msg'),
                  ip = self.request.remote_addr)
        log.put()
        mail.send_mail(sender="Applid <lazopm@gmail.com>",
                       to="Pablo Lazo <lazopm@gmail.com>",
                       subject="New Message from" + str(self.request.get('name')) + "(" +self.request.get('email')+ ")",
                       body=self.request.get('msg'))

#datastore image handler
class ViewImage(webapp2.RequestHandler):
    def get(self):
        if self.request.get('n'):
            project_key = ndb.Key('Project', int(self.request.get('id')))
            qry = Image.query(Image.name == self.request.get('n'), ancestor = project_key).get()
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(qry.image)

        else:
            project = Project.get_by_id(int(self.request.get('id')))
            if project.cover:
                self.response.headers['Content-Type'] = 'image/png'
                self.response.out.write(project.cover)
            else:
                self.response.out.write('No image')

#add image to project
class AddImage(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            if user.email()==ADMIN_GMAIL:
                image = Image(name = self.request.get('name'),
                              image = self.request.get('img'),
                              parent = ndb.Key('Project', int(self.request.get('project'))))
                image.put()
                self.redirect("/edit?project="+str(self.request.get('project')))
            else:
                self.error(401)
        else:
            self.redirect(users.create_login_url(self.request.uri))
#change project cover
class ChangeCover(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        if user:
            if user.email()==ADMIN_GMAIL:
                project = Project.get_by_id(int(self.request.get('project')))
                project.cover = (self.request.get('img'))
                project.put()
                self.redirect("/edit?project="+str(self.request.get('project')))
            else:
                self.error(401)
        else:
            self.redirect(users.create_login_url(self.request.uri))

#ajax description request handler
class Description(webapp2.RequestHandler):
    def get(self):
        project = Project.get_by_id(int(self.request.get('project')))
        desc = project.full_description
        self.response.out.write(desc.replace('<img src="','<img src="image?id='+self.request.get('project')+'&n='))

#404 error handler
class NotFound(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('404.html')
        self.response.write(template.render())

app = webapp2.WSGIApplication([
    ('/', Main),
    ('/portfolio', Portfolio),
    ('/new', NewProject),
    ('/edit', EditProject),
    ('/image', ViewImage),
    ('/message', Message),
    ('/addimg', AddImage),
    ('/changecover', ChangeCover),
    ('/desc', Description),
    ('/.*', NotFound)
], debug=True)
