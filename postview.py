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

class PostDisplay(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user is None:
			pass

		postid = self.request.get("postid")
		giftImageList =[]
		giftArticleList = []
		giftHyperinkList = []
		commentTimeList = []

		postQuery= Post.query()
		for post in postQuery:
			print "in post query"
			if post.id == postid:
				postwant=post
				break
		
		if user in postwant.savedList:
			Postsave = True
		else:
			Postsave = False


		if post.creator == user:
			OwnerLogin = True
		else:
			OwnerLogin =False 

		for gift in postwant.giftList:
			# print "length"
			# print len(postwant.giftList)
			# print "what is gift"
			# print gift.hyperLink
			# print "imageurl"
			# print images.get_serving_url(gift.image)
			
			giftImageList.append(images.get_serving_url(gift.image))
			giftArticleList.append(gift.article)
			giftHyperinkList.append(str(gift.hyperLink))

		for item in postwant.commentList:
			# Sun Dec 13 2015 20:15:57 GMT-0600 (CST)
			ttime = '{0:%a} {0:%b} {0:%d} {0:%Y} {0:%X}'.format(item.date)+" GMT-0600 (CST)"
			commentTimeList.append(ttime)

		template_values = {
			'loginURL':users.create_login_url(self.request.uri),
		    'logoutURL': users.create_logout_url('/'),
		    'user' : user,
		    'postwant':postwant,
		    'giftImageList':giftImageList,
		    'giftArticleList':giftArticleList,
		    'giftHyperinkList':giftHyperinkList,
		    'OwnerLogin':OwnerLogin,
		    'Postsave':Postsave,
		    'commentTimeList':commentTimeList

		}
		template = JINJA_ENVIRONMENT.get_template('post.html')
		self.response.write(template.render(template_values))

		#display PostView

class PostCreate(webapp2.RequestHandler):
	def get(self):
		#create Post
		#hidden when not login

		user = users.get_current_user()
		if user is None:
			pass

		template_values = {
			'loginURL':users.create_login_url(self.request.uri),
		    'logoutURL': users.create_logout_url('/'),
		    'user' : user
		}
		template = JINJA_ENVIRONMENT.get_template('createpost.html')
		self.response.write(template.render(template_values))
		

class PostCreateHandler(webapp2.RequestHandler):
	def post(self):
		hashid = hash(time.time())
		user = users.get_current_user()
		allTag = self.request.get("tags")
		tagList = allTag.split(" ")

		#print "taglist",tagList
		# print "name is "
		# print self.request.get("name")

		post = Post(id = str(hashid),
					name = self.request.get("name"),
					creator = user,
					savedCount = 0,
					savedList =[],
					sharetoSocialCount = 0,
					commentList = [],
					tags = tagList,
					giftList=[])
		post.put()

		params = urllib.urlencode({'postid': hashid})
		self.redirect('/GiftAdd/'+str(hashid))
		# self.redirect('/GiftAdd?'+params)

class CommentHandler(webapp2.RequestHandler):
	def post(self):
		user = users.get_current_user()
		if user is None:
			pass

		comment = self.request.get("comment")
		postid = self.request.get("postid")


		NewComment = Comment(creator=user,
			content=comment)
		NewComment.put()

		print "comment"
		print comment
		
		# print "postid"
		# print postid

		postQuery= Post.query()
		for post in postQuery:
			if post.id == postid:
				postwant=post
				break

		postwant.commentList.append(NewComment)
		postwant.put()

		params = urllib.urlencode({'postid': postid})
		self.redirect('/Post?'+params)



class PostSave(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user is None:
			pass

		postid = self.request.get("postid")
		print "postid"
		print postid

		postQuery= Post.query()
		for post in postQuery:
			if post.id == postid:
				postwant=post
				break

		if user in postwant.savedList:
			postwant.savedList.remove(user)
			postwant.savedCount=postwant.savedCount-1
		else:
			postwant.savedList.append(user)
			postwant.savedCount=postwant.savedCount+1
		
		postwant.put()
		print "IN post save"

		self.response.write(postwant.savedCount)
'''
class PostSaveDelete(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user is None:
			pass

		postid = self.request.get("postid")
		print "postid"
		print postid

		postQuery= Post.query()
		for post in postQuery:
			if post.id == postid:
				postwant=post
				break

		if user in postwant.savedList:
			postwant.savedList.remove(user)
			postwant.savedCount=postwant.savedCount-1
			postwant.put()
			print "IN post save Delete"

		self.response.write(postwant.savedCount)
'''


class PostShare(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		# if user is None:
		# 	pass

		postid = self.request.get("postid")
		postQuery= Post.query()
		for post in postQuery:
			if post.id == postid:
				postwant=post
				break
		
		print "IN post share"

		postwant.sharetoSocialCount=postwant.savedCount+1
		postwant.put()
		self.response.write(postwant.sharetoSocialCount)






