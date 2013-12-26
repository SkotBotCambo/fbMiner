'''
	This python module is used for data mining via the facebook-sdk python module
	for the Cornell University Social Media Lab and Northwestern University Social
	Media Lab
'''

import facebook
import json
import time

global ACCESS_TOKEN
global confession_id
confession_id = '618332588183265'
def set_token(string):
	ACCESS_TOKEN = string

def get_data(token):
	ACCESS_TOKEN = token
	num_pages = 1
	posts = []
	g = facebook.GraphAPI(ACCESS_TOKEN)
	# get initial page
	page1 = g.get_connections(confession_id, "feed", limit=1000)
	posts += page1['data']
	nextString = page1['paging']['next']
	next = nextString.split("until=")[-1]
	while True:
		print "page : " + str(num_pages)
		time.sleep(1)
		page = g.get_connections(confession_id, "feed", limit=1000, until=next)
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

def getLikes(post_id, token):
	like_arr = [] # 1st col : post_id, 2nd col : person who liked
	num_likes = 0
	ACCESS_TOKEN = token
	g = facebook.GraphAPI(ACCESS_TOKEN)
	like_obj = g.get_connections(post_id, "likes", limit=1000)
	num_likes = len(like_obj['data'])
	for liker in like_obj['data']:
		like_arr.append(liker['name'])
	time.sleep(2)
	return num_likes, like_arr

def getArr(posts, token):
	arr = []
	header = "post_id, time, message, type"
	arr.append(header)
	count = 0
	for p in posts:
		print "post #" + str(count)
		count += 1
		post_id = ''
		time = ','
		message = ','
		likes = ','
		post_type = ','
		try:
			post_id += p['id']
		except KeyError as ke:
			print ke
		try:
			time += p['created_time']
		except KeyError as ke:
			print ke
		try:
			message += p['message']
		except KeyError as ke:
			print ke
		try:
			post_type += p['type']
		except KeyError as ke:
			print ke
		num_likes, likers = getLikes(post_id, token)
		likes += str(num_likes)
		row = [post_id, time, message, likes, post_type]
		arr.append(row)
	return arr

# method for getting common data from each post and converting to an array
'''def get_comments(posts, token):
	comments = []
	ACCESS_TOKEN = token
	g = facebook.GraphAPI(ACCESS_TOKEN)
	posts_w_comments = 0
	comments = 0
	for p in posts:
		if 'comments' in p['data'].keys():
'''