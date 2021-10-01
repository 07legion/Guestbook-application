import webapp2
from urls import url_patterns

app = webapp2.WSGIApplication(url_patterns, debug = True)