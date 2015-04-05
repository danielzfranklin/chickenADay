import webapp2
from google.appengine.api import users

import models

MANDRILL_KEY = "Ke3oLmG_hC3qSGR-P0-dkg"

def sendMandrillEmail(dict):
    
    url = "https://mandrillapp.com/api/1.0/messages/send.json"
    result = urlfetch.fetch(url=url,
        payload=json.dumps(json),
        method=urlfetch.POST,
        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    
class SendDailyEmails(webapp2.RequestHandler):
    def get(self):
        imageUrl = "http://imgs.xkcd.com/comics/xkcloud.png"
        users = models.User.query()

        sendTo = [];

        for user in users:
            sendTo.append({""})

            sendMandrillEmail(
                {
                    "key": MANDRILL_KEY,
                    "template_name": "",
                    "template_content": [
                        {
                            "name": "example name",
                            "content": "example content"
                        }
                    ],
                    "message": {
                        "html": "<p>Example HTML content</p>",
                        "text": "Example text content",
                        "subject": "example subject",
                        "from_email": "message.from_email@example.com",
                        "from_name": "Example Name",
                        "to": [
                            {
                                "email": "recipient.email@example.com",
                                "name": "Recipient Name",
                                "type": "to"
                            }
                        ],
                        "headers": {
                            "Reply-To": "message.reply@example.com"
                        },
                        "important": false,
                        "track_opens": null,
                        "track_clicks": null,
                        "auto_text": null,
                        "auto_html": null,
                        "inline_css": null,
                        "url_strip_qs": null,
                        "preserve_recipients": null,
                        "view_content_link": null,
                        "bcc_address": "message.bcc_address@example.com",
                        "tracking_domain": null,
                        "signing_domain": null,
                        "return_path_domain": null,
                        "merge": true,
                        "merge_language": "mailchimp",
                        "global_merge_vars": [
                            {
                                "name": "merge1",
                                "content": "merge1 content"
                            }
                        ],
                        "merge_vars": [
                            {
                                "rcpt": "recipient.email@example.com",
                                "vars": [
                                    {
                                        "name": "merge2",
                                        "content": "merge2 content"
                                    }
                                ]
                            }
                        ],
                        "tags": [
                            "password-resets"
                        ],
                        "subaccount": "customer-123",
                        "google_analytics_domains": [
                            "example.com"
                        ],
                        "google_analytics_campaign": "message.from_email@example.com",
                        "metadata": {
                            "website": "www.example.com"
                        },
                        "recipient_metadata": [
                            {
                                "rcpt": "recipient.email@example.com",
                                "values": {
                                    "user_id": 123456
                                }
                            }
                        ],
                        "attachments": [
                            {
                                "type": "text/plain",
                                "name": "myfile.txt",
                                "content": "ZXhhbXBsZSBmaWxl"
                            }
                        ],
                        "images": [
                            {
                                "type": "image/png",
                                "name": "IMAGECID",
                                "content": "ZXhhbXBsZSBmaWxl"
                            }
                        ]
                    },
                    "async": false,
                    "ip_pool": "Main Pool",
                    "send_at": "example send_at"
                }
            )


app = webapp2.WSGIApplication([
    ("/send", SendDailyEmails)
], debug=True)
