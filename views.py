# CRUD #
import webapp2
import logging
from google.appengine.api import taskqueue
from models import GuestbookModel

class GuestbookHandler(webapp2.RequestHandler):
	def get(self):
		data = {'greeting': self.request.get('greeting')}
		task = taskqueue.add(url = '/getData', method = 'GET', params = data)

	def post(self):
		data = {
			'author': self.request.get('author'),
			'email': self.request.get('email'),
			'greeting': self.request.get('greeting'),
			'publishedDate': self.request.get('publishedDate'),
			'indexName': self.request.get('indexName')
		}
		task = taskqueue.add(url = '/insertData', method = 'POST', params = data)

	def put(self):
		data = {
			'email': self.request.get('email'), 
			'newAuthor': self.request.get('newAuthor')
		}
		task = taskqueue.add(url = '/updateData', method = 'PUT', params = data)

	def delete(self):
		data = {
			'email': self.request.get('email'), 
			'author': self.request.get('author')
		}
		task = taskqueue.add(url = '/deleteData', method = 'DELETE', params = data)