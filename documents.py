import webapp2
import worker
import logging
from google.appengine.api import search

def createDocument(author, email, greeting, publishedDate):
	document = search.Document(
		fields = [
			search.TextField(name = 'author', value = author),
			search.TextField(name = 'email', value = email),
			search.TextField(name = 'greeting', value = greeting), 
			search.DateField(name = 'publishedDate', value = worker.convert_to_date(publishedDate))
		]
	)
	return document

def getIndex(indexName):
	return search.Index(indexName)

def addDocument(document, indexName):
	indexName.put(document)
	return indexName

def searchDocuments(index, querySearch):
	results = index.search(querySearch)
	return [document for document in results]

def deleteIndex(index):
	while True:
		documentIds = [document.doc_id for document in index.get_range(ids_only = True)]
		if not documentIds: 
			break
		index.delete(documentIds)
	index.delete_schema()

def deleteDocument(index, documentIds):
	index.delete(documentIds)

class documentsHandler(webapp2.RequestHandler):
	def get(self):
		try:
			indexName = self.request.get('indexName')
			querySearch = self.request.get('search')
			index = getIndex(indexName)	
			searchResults = searchDocuments(index, querySearch)
			result = []
			for doc in searchResults:
				temp = []
				for itr in doc.fields:
					temp.append(itr.value)
				result.append(temp)
			
			logging.info(result)
			self.response.out.write(result)
		except Exception as e:
			logging.info(e)
	
	def delete(self):
		try:
			indexName = self.request.get('indexName')
			documentId = self.request.get('docId')
			index = getIndex(indexName)		
			if documentId == '':
				deleteIndex(index)
			else:
				deleteDocument(index, documentId)
		except Exception as e:
			logging.info(e)
		self.response.out.write("Data deleted!")