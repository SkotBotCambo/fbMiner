'''
	This python module is used for data mining via the facebook-sdk python module
	for the Cornell University Social Media Lab and Northwestern University Social
	Media Lab
'''

import facebook
from facepy.utils import get_extended_access_token
import json
from time import sleep
import urllib2
import datetime

global ACCESS_TOKEN
global confession_id
confession_id = '618332588183265'
global APP_ID
APP_ID = "463500207102372"
global APP_SECRET
APP_SECRET = "863524a429198f237fc09d3dbb2f5c04"

class scraper_tool:
	app_id = APP_ID # from the facebook app development site
	app_secret = APP_SECRET # from the facebook app development site
	user_token = '' # short token that generally expires in 2 hours
	g = facebook.GraphAPI()
	expire = ''  # sometimes you get back an expiration date with setLongToken
	long_token = '' #token that expires in 60 days
	page_id = confession_id #the id of the page that will be scraped
	wait = 0 # amount of time in seconds to wait in between query tasks
			# good for avoiding accidentally exceeding the API request limit
	limit_num = 100 # number of requests pulled from each query

	def setPageId(self, ID):
		self.page_id = ID

	def setShortToken(self, token):
		self.user_token = token
		self.g = facebook.GraphAPI(token)

	def expires(self):
		print self.expires
	def setLongToken(self, token):
		''' got this from the following site:
			http://fearofcoding.blogspot.com/2012/10/python-script-to-fetch-messages-from.html
		'''
		lt, expires_at = get_extended_access_token(token, self.app_id, self.app_secret)
		self.expires = expires_at
		print "expires : " + str(expires_at)
		self.long_token = lt
		self.g = facebook.GraphAPI(self.long_token)

	def getGraphAPI(self):
		''' use this to get the facebook.GraphAPI() object back to use directly'''
		return self.g
	
	def setLongTokenFromFile(self, fileName):
		fileIn = open(fileName, 'rb')
		lt = fileIn.readlines()[0]
		self.long_token = lt
		self.g = facebook.GraphAPI(self.long_token)

	def writeLongTokenToFile(self, fileName):
		fileOut = open('fileName', 'wb')
		fileOut.write(self.long_token)

	def get_data(self):
		''' gets general data from site '''
		num_pages = 1
		posts = []
		# get initial page
		page1 = self.g.get_connections(self.page_id, "feed", limit=self.limit_num)
		posts += page1['data']
		nextString = page1['paging']['next']
		next = nextString.split("until=")[-1]
		while True:
			print "page : " + str(num_pages)
			sleep(1)
			while True:
				try:
					page = self.g.get_connections(self.page_id, "feed", limit=self.limit_num, until=next)
				except facebook.GraphAPIError as gep:
					print gep
					token = raw_input("enter new token : " )
					g = facebook.GraphAPI(token)
				except urllib2.URLError as urlerr:
					print urlerr
					print "waiting 10 minutes at :"
					print datetime.datetime.now()
					sleep(1800)
					g = facebook.GraphAPI(token)
				else:
					break
			if 'data' in page.keys():
				posts += page['data']
				num_pages+=1
			else:
				break
			if 'paging' in page.keys():
				if 'next' in page['paging']:
					nextString = page['paging']['next']
					next = nextString.split("until=")[-1]
				else:
					break
			else:
				break
		return posts

	def getArr(self, posts=0):
		'''
			Input will be the posts that are returned from get_data()
			returns two separate 2D array/lists, post_rows, and comment_rows
			use arr_to_string() to get ready for exporting to a .csv file
		'''
		if posts == 0:
			posts = get_data(token)
		post_rows = [['post_id', 'time', 'message', 'num_likes', 'num_comments', 'type']]
		comment_rows = [['post_id', 'comment_id', 'user_name', 'user_id', 'time', 'like_count', 'message']]
		count = 1
		num = len(posts)
		for p in posts:
			print "Post #" + str(count) + " out of " + str(num)
			count +=1
			likes = 0
			num_comms = 0
			message =''
			if 'message' in p.keys():
				message = p['message']
			if 'likes' in p.keys():
				while True:
					try:
						likes = getLikes(p['id'], self.g)
					except facebook.GraphAPIError as gep:
						print gep
						token = raw_input("enter new token : " )
						g = facebook.GraphAPI(token)
					except urllib2.URLError as urlerr:
						print urlerr
						print "waiting 10 minutes at :"
						print datetime.datetime.now()
						sleep(1800)
						g = facebook.GraphAPI(token)
					else:
						sleep(self.wait)
						break

			if 'comments' in p.keys():
				while True:
					try:
						comments = getComments(p['id'], g)
					except facebook.GraphAPIError as gep:
						print gep
						token = raw_input("enter new token : " )
						g = facebook.GraphAPI(token)
					except urllib2.URLError as urlerr:
						print urlerr
						print "waiting 10 minutes at :"
						print datetime.datetime.now()
						sleep(1800)
						g = facebook.GraphAPI(token)
					else:
						break
				num_comms = len(comments)
				for c in comments:
					comment_rows.append(c)

			post_row = [p['id'],
						p['created_time'],
						message,
						likes,
						num_comms,
						p['type']]
			post_rows.append(post_row)
		return post_rows, comment_rows

	def arr_to_string(self, arr):
		new_rows = []
		for p in arr:
			new_row = []
			for x in p:
				val = x
				stringVal = ''
				try:
					if type(x) is type(u''):
						stringVal = val.encode('ascii', 'ignore').replace('\n', ' ')
					else:
						stringVal = str(x).encode('ascii','ignore')
				except UnicodeEncodeError as uee:
					print uee
					print x
					raw_input('press any key')
				new_row.append(stringVal)
			new_rows.append(new_row)
		return new_rows
	
	def getCommentData(self, posts):
		comments = []
		count = 1
		for p in posts:
			print "Post #" + str(count)
			count += 1
			if 'comments' in p.keys():
				while True:
					try:
						comms = getComments(post_id, self.g)
					except facebook.GraphAPIError as gep:
						print gep
						token = raw_input("enter new token : " )
						self.g = facebook.GraphAPI(token)
					except urllib2.URLError as urlerr:
						print urlerr
						print "waiting 10 minutes at :"
						print datetime.datetime.now()
						sleep(1800)
						self.g = facebook.GraphAPI(token)
					else:
						break
				for comm in comms:
					comments.append(comm)
		return comments

	def getLikes(self, post_id, wait=0):
		num_likes = 0
		like_obj = self.g.get_connections(post_id, "likes", limit=self.limit_num)
		num_likes = len(like_obj['data'])
		if wait > 0:
			sleep(self.wait)
		return num_likes

	def getLikeData(self, posts):
		num_likes_arr = []
		like_posters = []
		count = 1
		for p in posts:
			print "post #" + str(count)
			count += 1
			post_id = p['id']
			if 'likes' in p.keys():
				while True:
					try:
						num_likes = getLikes(post_id)
					except facebook.GraphAPIError as gep:
						print gep
						token = raw_input("enter new token : " )
						g = facebook.GraphAPI(token)
					except urllib2.URLError as urlerr:
						print urlerr
						print "waiting 10 minutes at :"
						print datetime.datetime.now()
						sleep(1800)
						g = facebook.GraphAPI(token)
					except ValueError as ve:
						print ve
						sleep(180)
					else:
						break
				num_likes_arr.append(num_likes)
			else:
				num_likes_arr.append(0)
		return num_likes_arr

	def getComments(self, post_id):
		''' for a post_id, look up all comments and get the comment_id, user_name, user_id, time, num_likes, and message '''
		comments = []
		comm_obj = self.g.get_connections(post_id, "comments", limit=self.limit_num)
		for comm in comm_obj['data']:
			comment = [post_id, comm['id'],
					comm['from']['name'],
					comm['from']['id'],
					comm['created_time'],
					comm['like_count'],
					comm['message']]
			comments.append(comment)
		if self.wait > 0:
			sleep(self.wait)
		return comments