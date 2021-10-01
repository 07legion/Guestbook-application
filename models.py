from google.appengine.ext import ndb

class GuestbookModel(ndb.Model):
	email = ndb.StringProperty(required = True)
	author = ndb.StringProperty(required = True)
	greeting = ndb.StringProperty(required = True)
	publishedDate = ndb.DateProperty(required = True) 