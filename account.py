import os;

import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb

import models


class RegisterPageHandler(webapp2.RequestHandler):
    def get(self):
        thisPerson = users.get_current_user()

        uid = thisPerson.user_id()
        email = thisPerson.email()
        name = thisPerson.nickname()

        # record their name in a cookie
        self.response.headers.add_header('Set-Cookie', "name=" + name + "; Path=/")


        # save this user in the database
        thisUser = models.User(id=uid, name=name, email=email)
        key = thisUser.put()

        self.response.out.write(template.render("templates/register.html", {"name": name, "email": email, "signout": users.create_logout_url("/")}))

app = webapp2.WSGIApplication([
    ('/account', RegisterPageHandler),
], debug=True)
