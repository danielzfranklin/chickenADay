from google.appengine.ext import ndb

class User(ndb.Model):
    uid = ndb.StringProperty()
    email = ndb.StringProperty()
    name = ndb.StringProperty()
