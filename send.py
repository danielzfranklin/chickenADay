import webapp2
from google.appengine.api import users

import models

MANDRILL_KEY = "Ke3oLmG_hC3qSGR-P0-dkg"

def sendMandrillEmail(json):
    
    url = "https://mandrillapp.com/api/1.0/messages/send.json"
    result = urlfetch.fetch(url=url,
        payload=json.dumps(json),
        method=urlfetch.POST,
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    
class SendEmails(webapp2.RequestHandler):
    def get(self):
        imageUrl = "http://imgs.xkcd.com/comics/xkcloud.png"
        users = models.User.query()

        for user in users:
            emailHTML = """
<table><thead></thead><tbody>
<tr><td>Hello {},</td></tr>
<tr><td></td></tr>
<tr><td>Since you signed up for a chicken picture a day, here is your image:</td></tr>
<tr><td><img src="{}"></td></tr>
<tr><td></td></tr>
<tr><td>Enjoy,</tr></tr>
<tr><td>Daniel</td></tr>
</tbody></table>
""".format(user.name,imageUrl)

            sendMandrillEmail({
                "key": MANDRILL_KEY,
                    "message": {
                        "html": emailHTML,
                        "subject": user.name+" - Chicken A Day",
                        "from_email": "danielf@openmailbox.org",
                        "from_name": "Daniel Franklin",
                        "to": [
                            {
                                "email": user.email
                            }
                       ]
                    }
            })


app = webapp2.WSGIApplication([
    ("/send", SendEmails)
], debug=True)
