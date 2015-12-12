import cgi
import urllib
import os

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2
import jinja2

import re
import json
from collections import defaultdict
import hashlib
from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import memcache
from google.appengine.api import search
from google.appengine.api import images
from google.appengine.api import mail
import time
import datetime
import operator

from structure import Comment
from structure import Gift
from structure import Post


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__),'templates')),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
'''
class CreatePost(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
        if user is None:
            self.redirect('/')
        
        template_values = {
            'logoutURL': users.create_logout_url('/'),
            'user' : user
        }
        template = JINJA_ENVIRONMENT.get_template('Create.html')
        self.response.write(template.render(template_values))

class CreatePostHandler(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		if user is None:
			self.redirect('/')




		pass

'''




