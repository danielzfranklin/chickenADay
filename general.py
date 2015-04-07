import webapp2
from google.appengine.ext.webapp import template

class TermsHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render("templates/terms.html", {}))
class PrivacyHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render("templates/privacy.html", {}))
class ReportBadHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(template.render("templates/reportBad.html", {}))

app = webapp2.WSGIApplication([
    ('/terms', TermsHandler),
    ("/privacy", PrivacyHandler),
    ("/reportBad", ReportBadHandler)
], debug=True)