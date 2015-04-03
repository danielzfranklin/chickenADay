import webapp2
from google.appengine.api import users

import models

class RegisterPageHandler(webapp2.RequestHandler):
    def get(self):
        thisPerson = users.get_current_user()
        
        uid = thisPerson.user_id()
        email = thisPerson.email()
        name = thisPerson.nickname()

        #record their name in a cookie
        self.response.headers.add_header('Set-Cookie', "name="+name+"; Path=/" )

        #save this user in the database
        thisUser = models.User(name = name, email = email, uid = uid)
        thisUser.put()

        self.response.write("UID: "+uid+" Email: "+email+" Name: "+name)

app = webapp2.WSGIApplication([
    ('/account', RegisterPageHandler),
], debug=True)
