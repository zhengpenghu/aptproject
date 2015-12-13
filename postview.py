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



		template_values = {
			'loginURL':users.create_login_url(self.request.uri),
		    'logoutURL': users.create_logout_url('/'),
		    'user' : user,
		    'postwant':postwant,
		    'giftImageList':giftImageList,
		    'giftArticleList':giftArticleList,
		    'giftHyperinkList':giftHyperinkList,
		    'OwnerLogin':OwnerLogin,
		    'Postsave':Postsave

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
		self.redirect('/GiftAdd/'+hashid)
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

class PostDelete(webapp2.RequestHandler):
	def post(self):
		deletePostlist =[]
		deletePostlist=self.request.get_all('deleteCheckbox')
		post_query = Post.query()

		for p in post_query:
			if p.id in deletePostlist:
				for i in range(0,len(p.giftList)):
					Gift.delete_serving_url(p.giftList[i].image)
					blobstore.delete(p.giftList[i].image,rpc=None)
				p.key.delete()
		self.redirect('/manage')


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






