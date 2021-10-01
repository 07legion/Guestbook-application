import webapp2
import logging
from models import GuestbookModel 
import worker

class notificationHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write("Notifying after every 1 minute!")