import json

import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

import models
import passwords

def sendMandrillEmail(dict):

    url = "https://mandrillapp.com/api/1.0/messages/send-template.json"
    result = urlfetch.fetch(url=url,
        payload=json.dumps(dict),
        method=urlfetch.POST,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    return result.content

class RegisterPageHandler(webapp2.RequestHandler):
    def get(self):
        person = users.get_current_user()

        uid = person.user_id()
        email = person.email()
        name = person.nickname()

        # record their name in a cookie
        self.response.headers.add_header('Set-Cookie', "name=" + name + "; Path=/")

        query = models.User.query(models.User.uid==uid) #make a query by uid
        results = query.fetch() # lookup this user

        if len(results) == 0: #this user is not in the database
            user = models.User(id=uid, uid=uid, name=name, email=email, confirmed=False)

        else:
            user = results[0]

        if user.confirmed == False:
            self.response.out.write(template.render("templates/register.html", {"name": name, "email": email, "signout": users.create_logout_url("/"), "alreadyConfirmed": False})) #give them the "you just got sent a confirmation email message

            sendMandrillEmail(
                {
                    "key": passwords.MANDRILL_API_KEY,
                    "template_name": "chicken-a-day-subscription-confirmation",
                    "template_content": [],
                    "message": {
                        "to": [
                            {
                                "email": email,
                                "type": "to",
                                "name": name
                            }
                        ],
                        "important": False,
                        "track_opens": True,
                        "track_clicks": True,
                        "auto_text": False,
                        "auto_html": False,
                        "inline_css": False,
                        "url_strip_qs": True,
                        "preserve_recipients": False,
                        "view_content_link": True,
                        "merge_language": "mailchimp",
                        "global_merge_vars": [],
                        "merge_vars": [
                            {
                                "rcpt": email,
                                "vars": [
                                    {"name": "CONFIRM_URL", "content": "https://chickenaday.appspot.com/confirm?email="+email}
                                ]
                            }
                        ],
                        "tags": [
                            "chicken-a-day-subscription-confirmation"
                        ],
                        "google_analytics_domains": [],
                        "metadata": {},
                        "recipient_metadata": [],
                        "attachments": [],
                        "images": []
                    },
                    "async": True,
                }
            )
        else:
            self.response.out.write(template.render("templates/register.html", {"name": name, "email": email, "signout": users.create_logout_url("/"), "signoutToHere": users.create_logout_url("/account"), "alreadyConfirmed": True})) #give them the "you just got sent a confirmation email message

        key = user.put() # save any changes to the user that were made

class ConfirmPageHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get("email")

        query = models.User.query(models.User.email==email)
        results = query.fetch()

        if len(results) == 0:
            parameters = {"success": False, "email": email}
        else:
            user = results[0]
            parameters = {"success": True, "email": user.email, "name": user.name}

            user.confirmed = True # mark that the user has now confirmed
            user.put() # save that change

        self.response.out.write(template.render("templates/confirm.html", parameters))

class UnsubscribePageHandler(webapp2.RequestHandler):
    def get(self):
        email = self.request.get("email")

        if email == "":
            parameters = {"result": "noEmail"}
        else:
            query = models.User.query(models.User.email == email)
            results = query.fetch()

            if len(results) == 0:
                parameters = {"result": "noRecord", "email": email}
            else:
                user = results[0]
                parameters = {"result": "success", "email": user.email, "name": user.name}

                user.key.delete()
        self.response.out.write(template.render("templates/unsubscribe.html", parameters))

app = webapp2.WSGIApplication([
    ('/account', RegisterPageHandler),
    ('/confirm', ConfirmPageHandler),
    ("/unsubscribe", UnsubscribePageHandler)
], debug=True)
