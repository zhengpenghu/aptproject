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

class Comment(ndb.Model):
	#replyto = ndb.StructuredProperty(Comment);
	#can remember which comment you reply to
	creator = ndb.UserProperty();
	content = ndb.StringProperty();
	date = ndb.DateTimeProperty(auto_now_add = True);

class Gift(ndb.Model):
	date = ndb.DateTimeProperty(auto_now_add = True);
	article = ndb.StringProperty()
	image = ndb.BlobKeyProperty()
	price = ndb.StringProperty()
	hyperLink = ndb.StringProperty()		#true for selling post. false for social sharing
	

'''
Post has a list of Gift
Post has a list of Comment

'''

class Post(ndb.Model):
	id = ndb.StringProperty();
	name = ndb.StringProperty();
	creator = ndb.UserProperty();
	savedCount = ndb.IntegerProperty();
	savedList = ndb.UserProperty(repeated = True);#store the list of saved users
	sharetoSocialCount = ndb.IntegerProperty();
	lastUpdateDate = ndb.DateTimeProperty(auto_now_add=True);
	commentList = ndb.StructuredProperty(Comment, repeated=True);
	tags = ndb.StringProperty(repeated = True);
	giftList = ndb.StructuredProperty(Gift, repeated = True);












