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

class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user is None:
			pass
		PostsList = []
		PostPreviewList =[]

		for post in Post.query().order(Post.lastUpdateDate):#fetch(16)
			PostsList.append(post)
			try:
				previewImage = images.get_serving_url(post.giftList[0].image)
			except Exception,e:
				previewImage = "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTt9ALzNY6Ef_7To_OnTLEkUpXYu6jW6-DB4oi6JRxD2mdBdD293lcUdg"
			# if previewImage is None:
			# 	pass

			PostPreviewList.append(previewImage)

		template_values = {
			'loginURL':users.create_login_url(self.request.uri),
			'logoutURL': users.create_logout_url('/'),
			'PostsList' : PostsList,
			'PostPreviewList':PostPreviewList,
			'user':user,
		}
		template = JINJA_ENVIRONMENT.get_template('mainpage.html')
		
		self.response.write(template.render(template_values))


class DynamicLoadHandler(webapp2.RequestHandler):
	def get(self):
		AppendList =[];
		StartIndex = self.request.get("index")
		#index is 16,32,48,64...
		
		fullList = Post.query().order(Post.lastUpdateDate).fetch(StartIndex+16)
		AppendList = fullList[StartIndex:StartIndex+16]

		#for post in Post.query().order(Post.lastUpdateDate).fetch(StartIndex+16):
			#AppendList









