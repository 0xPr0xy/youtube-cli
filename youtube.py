#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
import sys
import random

from youtube_player import YoutubePlayer
# my player, uses urwid and vlc ^^

import gdata.youtube.service
# https://developers.google.com/youtube/2.0/developers_guide_protocol_api_query_parameters

from ytdl import ytdl
from ytstr import ytstr
# https://bitbucket.org/rg3/youtube-dl/wiki/Home


class YoutubeClient:
	

	def __init__(self,keyword,q,order,num_results,shuffle=None):
		
		keywords = ['search', 'download', 'stream']
		if keyword in keywords: self.keyword = keyword
		else: sys.exit('invalid keyword')
		
		self.q = q
		self.hd = True
		ordering_key = {'rating':'rating', 'viewcount':'viewCount','relevance':'relevance'}
		ordering = ['rating','viewcount','relevance']
		
		if order in ordering: self.order = ordering_key[order]
		else: sys.exit('invalid ordering')

		try: self.num = int(num_results)
		except Exception as e: sys.exit('invalid number %s' %e)

		try: self.shuffle = shuffle
		except IndexError: self.shuffle = False

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
		query.vq = self.q
		query.max_results = self.num
		query.start_index = 1
		query.racy = 'exclude'
		query.orderby = self.order
		feed = self.client.YouTubeQuery(query)
		if self.shuffle:
			random.shuffle(feed.entry)
		command = self.keyword

		if command == 'download':
			self.download(feed)
		if command == 'stream':
			self.stream(feed)
		if command == 'search':
			self.search(feed)

call = YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])