import webapp2
import views
import worker
import cronJobs
import documents

url_patterns = [
	webapp2.Route('/', views.GuestbookHandler), 
	webapp2.Route('/getData', worker.getDataHandler),
	webapp2.Route('/insertData', worker.insertDataHandler),
	webapp2.Route('/updateData', worker.updateDataHandler),
	webapp2.Route('/deleteData', worker.deleteDataHandler), 
	webapp2.Route('/notification', cronJobs.notificationHandler), 
	webapp2.Route('/documents', documents.documentsHandler)
]