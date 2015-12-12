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

class SearchHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		searchContents = self.request.get("searchContent")

		if searchContents != "":
			searchWords = searchContents.split(' ')
			for i in range(0,len(searchWords)):
				searchWords[i]=str(searchWords[i].lower())
			print searchWords
		
		PostsList = []
		PostPreviewList=[]
		
		for post in Post.query().order(Post.lastUpdateDate):
			p_word =[]
			for item in post.name.split(' '):
				p_word.append(item.lower())
			for item in post.tags:
				p_word.append(item.lower())

			for item in p_word:
				if item in searchWords:
					PostsList.append(post)
					try:
						previewImage = images.get_serving_url(post.giftList[0].image)
					except Exception,e:
						previewImage = "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTt9ALzNY6Ef_7To_OnTLEkUpXYu6jW6-DB4oi6JRxD2mdBdD293lcUdg"
					PostPreviewList.append(previewImage)

		template_values = {
			'loginURL':users.create_login_url(self.request.uri),
			'logoutURL': users.create_logout_url('/'),
			'PostsList' : PostsList,
			'PostPreviewList':PostPreviewList,
			'user':user,
		}
		template = JINJA_ENVIRONMENT.get_template('search.html')
		
		self.response.write(template.render(template_values))



		pass








