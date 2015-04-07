import time
import json

import webapp2
from google.appengine.api import users
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
    
class SendDailyEmails(webapp2.RequestHandler):
    def get(self):
        users = models.User.query(models.User.confirmed == True).fetch()
        photo = models.General.query(models.General.key == "dailyImage").fetch()[0]

        to = []
        mergeVars = [];
        globalMergeVars = [
            {"name": "PHOTO_URL", "content": photo.url},
            {"name": "PHOTO_AUTHOR", "content": photo.name},
            {"name": "PHOTO_PROFILE", "content": photo.profile}
        ]

        for user in users:
            mergeVars.append(
                {
                    "rcpt": user.email,
                    "vars": [
                        {"name": "NAME", "content": user.name},
                        {"name": "UNSUBSCRIBE", "content": "https://chickenaday.appspot.com/unsubscribe?email="+user.email}
                    ]
                }
            )

            to.append(
                {
                    "email": user.email,
                    "name": user.name,
                    "type": "to"
                }
            )

        sendMandrillEmail(
            {
                "key": passwords.MANDRILL_API_KEY,
                "template_name": "chicken-a-day",
                "template_content": [
                ],
                "message": {
                    "subject": "Chicken A Day for "+time.strftime("%d-%m-%y"),
                    "from_email": "contact@chickenaday.appspotmail.com",
                    "from_name": "Daniel F",
                    "to": to,
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
                    "global_merge_vars": globalMergeVars,
                    "merge_vars": mergeVars,
                    "tags": [
                        "chicken-a-day-daily"
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

app = webapp2.WSGIApplication([
    ("/send", SendDailyEmails)
], debug=True)
