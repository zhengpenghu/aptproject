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

class GiftAdd(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user is None:
			pass
		postid = self.request.get("postid")	
		upload_url = blobstore.create_upload_url('/UploadHandler/%s'%postid)

		template_values = {
			'loginURL':users.create_login_url(self.request.uri),
		    'logoutURL': users.create_logout_url('/'),
		    'user' : user,
		    'postid':postid,
		    'upload_url':upload_url
		}
		template = JINJA_ENVIRONMENT.get_template('giftadd.html')
		self.response.write(template.render(template_values))



'''
class GiftAddHandler(webapp2.RequestHandler):
	def post(self):
		postid = self.request.get("postid")
		upload_url = blobstore.create_upload_url('/UploadHandler/%s'%postid)

		image = 


		gift = Gift(hyperLink=self.request.get("Link"),
				article=self.request.get("article"),

			)
'''



#--InternalHandler--#
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self,postid):
		try:
			upload = self.get_uploads()
		except:
			assert(False)
			self.redirect('/')

		article = self.request.get("article")
		hyperLink= self.request.get("Link")
		# print "article"
		# print article
		# print "hyperLink"
		# print hyperLink
		# print "type of postid"
		# print type(postid)

		# print "length of upload"
		# print len(upload)
		# assert(False)

		post_query = Post.query()
		for s in post_query:
			if s.id==postid:
				for item in upload:
					gift=Gift()
					gift.image=item.key()
					print "item key"
					print item.key
					gift.article=article
					gift.hyperLink=hyperLink
					gift.put()

					s.giftList.append(gift)
					s.lastUpdateDate=gift.date
					s.put()
				break
				
		#assert(False)

		params = urllib.urlencode({'postid': postid})
		self.redirect('/Post?'+params)



