# Task Queues #
import webapp2
import logging
import documents
from datetime import datetime
from models import GuestbookModel
from google.appengine.api import search
from google.appengine.api import memcache

def convert_to_date(inputDate):
	return datetime.strptime(inputDate, '%d-%m-%Y').date()

def getGreetings(greetingQuery):
	listOfGreetings = []
	if greetingQuery == '': 
		greetings = GuestbookModel.gql("").order(-GuestbookModel.publishedDate)
	else: 
		greetings = GuestbookModel.gql("WHERE greeting =:1", greetingQuery).order(-GuestbookModel.publishedDate)
	for record in greetings: 
		listOfGreetings.append([record.author, record.email, record.greeting, record.publishedDate])
	return listOfGreetings

class getDataHandler(webapp2.RequestHandler):
	def get(self):
		result = {'success': False, 'msg': ''}
		try:
			greetingQuery = self.request.get('greeting')
			queryResult = memcache.get(greetingQuery)
			if queryResult is None:
				queryResult = getGreetings(greetingQuery)
				try:
					added = memcache.add(greetingQuery, queryResult, 300)
					if not added:
						logging.error('Memcache set failed.')
				except:
					logging.error('Memcache set failed - data larger than 1MB')

			result['success'] = True
			result['msg'] = queryResult
			logging.info(result)
			stats = memcache.get_stats()
			logging.info('hits: ' + str(stats['hits']))
			logging.info('misses: ' + str(stats['misses']))

		except Exception as e:
			result['msg'] = e
		self.response.out.write(result)

class insertDataHandler(webapp2.RequestHandler):
	def post(self):    
		result = {'success': False, 'msg': ''}
		try:
			guestbook = GuestbookModel()
			query = [self.request.get('author'), self.request.get('email'), self.request.get('greeting'), self.request.get('publishedDate'), self.request.get('indexName')]
			guestbook.author = query[0]
			guestbook.email = query[1]
			guestbook.greeting = query[2] 
			guestbook.publishedDate = convert_to_date(query[3])
			guestbook.put()
			result['msg'] = 'Data Inserted!'
			result['success'] = True
			logging.info(result)

			## Inserting into index 
			index = documents.getIndex(query[4])
			document = documents.createDocument(query[0], query[1], query[2], query[3])
			index = documents.addDocument(document, index)
			## 

		except Exception as e:
			result['msg'] = e
		self.response.out.write(result)

class updateDataHandler(webapp2.RequestHandler):
	def put(self):
		result = {'success': False, 'msg': ''}
		try:
			greetings = GuestbookModel.gql("where email =:1", self.request.get('email'))
			for greeting in greetings:
				greeting.author = self.request.get('newAuthor')
			greeting.put()
			result['msg'] = 'Data Updated!'
			result['success'] = True
			logging.info(result)
		except Exception as e:
			result['msg'] = e
		self.response.out.write(result)

class deleteDataHandler(webapp2.RequestHandler):
	def delete(self):
		result = {'success': False, 'msg': ''}
		try:
			greetings = GuestbookModel.gql("where email =:1 AND author =:2", self.request.get('email'), self.request.get('author'))
			greetings.get().key.delete()
			result['msg'] = 'Record Deleted!'
			result['success'] = True
			logging.info(result)
		except Exception as e:
			result['msg'] = e
		self.response.out.write(result)