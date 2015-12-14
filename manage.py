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

class Manage(webapp2.RequestHandler):
	#manage the posts created
	def get(self):
		user = users.get_current_user()
		if user is None:
			self.redirect('/')

		Postowned = []
		PostPreviewList =[]
		'''
			find out all posts&activity by a user
		'''
		
		for post in Post.query().order(-Post.lastUpdateDate):
			if post.creator == user:
				Postowned.append(post)
				try:
					previewImage = images.get_serving_url(post.giftList[0].image)
				except Exception,e:
					previewImage = "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcTt9ALzNY6Ef_7To_OnTLEkUpXYu6jW6-DB4oi6JRxD2mdBdD293lcUdg"
				PostPreviewList.append(previewImage)
		
		template_values = {
			'loginURL':users.create_login_url(self.request.uri),
			'logoutURL': users.create_logout_url('/'),
			'user' : user,
			'Postowned':Postowned,
			'PostPreviewList':PostPreviewList
		}
		template = JINJA_ENVIRONMENT.get_template('manage.html')
		self.response.write(template.render(template_values))

class PostDelete(webapp2.RequestHandler):
	def post(self):
		deletePostlist =[]
		deletePostlist=self.request.get_all('deleteCheckbox')
		post_query = Post.query()

		for p in post_query:
			if p.id in deletePostlist:
				for i in range(0,len(p.giftList)):
					images.delete_serving_url(p.giftList[i].image)
					blobstore.delete(p.giftList[i].image,rpc=None)
				p.key.delete()
		self.redirect('/manage')








