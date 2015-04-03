import webapp2

import models

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


app = webapp2.WSGIApplication([
    ('/', MainPageHandler),
], debug=True)
