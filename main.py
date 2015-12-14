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

from mainpage import MainPage

from manage import Manage
from manage import PostDelete

from postview import PostCreate
from postview import PostCreateHandler
from postview import PostDisplay
from postview import CommentHandler
from postview import PostSave
#from postview import PostSaveDelete
from postview import PostShare


from error import Error

from gift import GiftAdd
#from gift import GiftAddHandler
from gift import UploadHandler

from search import SearchHandler

Routes=[
        ('/', MainPage),
        ('/manage', Manage),
                ('/DeletePost',PostDelete),
        ('/PostCreate',PostCreate),
        	('/PostCreateHandler',PostCreateHandler),
        ('/Post',PostDisplay),
        	('/AddComment',CommentHandler),
                ('/PostShare',PostShare),
                ('/PostSave',PostSave),
                #('/PostSaveDelete',PostSaveDelete),
        ('/search',SearchHandler),
        ('/GiftAdd/([^/]+)',GiftAdd),
        	#('/GiftAddHandler',GiftAddHandler),
        	('/UploadHandler/([^/]+)',UploadHandler),
        ('/Error', Error)]

app = webapp2.WSGIApplication(Routes, debug=True)