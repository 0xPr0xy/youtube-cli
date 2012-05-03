#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
import sys
import random

from youtube_player import YoutubePlayer
# my player, uses urwid and vlc ^^

import gdata.youtube.service
# http://gdata-python-client.googlecode.com/hg/pydocs/gdata.youtube.service.html#YouTubeVideoQuery
# https://developers.google.com/youtube/1.0/developers_guide_python

from ytdl import ytdl
from ytstr import ytstr
# https://bitbucket.org/rg3/youtube-dl/wiki/Home


class YoutubeClient:
	

	def __init__(self,keyword,q,order,num_results,shuffle=None,time=None):
		
		keywords = ['search', 'download', 'stream']
		if keyword in keywords: self.keyword = keyword
		else: sys.exit('invalid keyword')
		
		self.q = q
	
		ordering_key = {'rating':'rating', 'viewcount':'viewCount','relevance':'relevance','published':'published'}
		ordering = ['rating','viewcount','relevance']
		if order in ordering: self.order = ordering_key[order]
		else: sys.exit('invalid ordering')
		
		try: self.num = int(num_results)
		except Exception as e: sys.exit('invalid number %s' %e)
		
		if shuffle is not None:	self.shuffle = shuffle
		else: self.shuffle = False

		times_key = {'today':'today','week':'this_week','month':'this_month','time':'all_time'}
		times = ['today', 'this_week', 'this_month', 'all_time']
		if time is not None and time in times: self.time = times_key[time]
		else: self.time = False

		self.client = gdata.youtube.service.YouTubeService()
		self.execute()


	def search(self,feed):

		for entry in feed.entry:
			try:
				print '\n[video] title: %s' % entry.title.text
				print '[video] url: %s' % entry.media.player.url
				print '[video] rating: %s' % entry.rating.average
				print '[video] view count: %s' % entry.statistics.view_count
				print '[video] id: %s' % entry.media.player.url.split('watch?v=').pop().split("&")[0]
			except Exception as e: 
				print('search failed:\nError: %s' % e)


	def download(self,feed):
		
		for entry in feed.entry:
			try:
				ytdl.main(entry.media.player.url)
			except Exception as e:
				print('download failed:\nError: %s' % e)


	def stream(self,feed):
		
		urls = []
		for entry in feed.entry:
			try:
				ytstr.main(entry.media.player.url)
			except ytstr.ReturnUrl as url:
				print '[youtube] Found location for video %s' %entry.title.text
				print '[youtube] URL: %s' %url
				urls.append(str(url))
			except Exception as e:
				print('download failed:\nError: %s' % e)
		player = YoutubePlayer(urls)


	def execute(self):
		
		query = gdata.youtube.service.YouTubeVideoQuery()	
		query.format = '5'
		query.hd = True
		query.vq = self.q
		query.max_results = self.num
		query.start_index = 1
		query.racy = 'exclude'
		query.orderby = self.order
		if self.time: query.time = self.time
		feed = self.client.YouTubeQuery(query)
		if self.shuffle: random.shuffle(feed.entry)
		command = self.keyword
		if command == 'download': self.download(feed)
		if command == 'stream':	self.stream(feed)
		if command == 'search':	self.search(feed)


if len(sys.argv) == 7:
	YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
if len(sys.argv) == 6:
	if sys.argv[5] == 'shuffle': YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], None)
	else: YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], None, sys.argv[5])
if len(sys.argv) == 5:
	YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])