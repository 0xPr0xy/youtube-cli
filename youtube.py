#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
import sys
import random


from youtube_player.youtube_player import YoutubePlayer
# the player, uses the vlc media player python bindings

import gdata.youtube.service
# http://gdata-python-client.googlecode.com/hg/pydocs/gdata.youtube.service.html#YouTubeVideoQuery
# https://developers.google.com/youtube/1.0/developers_guide_python

from stream import stream
from stream import download
# https://bitbucket.org/rg3/youtube-dl/wiki/Home

import urwid
# http://excess.org/urwid/reference.html


class ItemWidget (urwid.WidgetWrap):

	def __init__ (self, entry):
		""" Creates UI Element for every Entry"""

		if entry is not None:
			self.content = entry.media.player.url #limit content? [:25]
			self.item = [
				urwid.Padding(urwid.AttrWrap(
				urwid.Text('%s' % ( entry.title.text)),  'body', 'focus')),
				urwid.Padding(urwid.AttrWrap(
				urwid.Text('Rating:%s' % ( entry.rating.average)),  'body', 'focus'), left=10),
				urwid.Padding(urwid.AttrWrap(
				urwid.Text('Viewcount:%s' % ( entry.statistics.view_count )),  'body', 'focus'), left=5),
			]
		w = urwid.Columns(self.item)
		self.__super.__init__(w)

	def selectable (self):
		return True

	def keypress(self, size, key):
		return key



class YoutubeClient:

	def __init__(self,keyword,q,order,num_results,shuffle=None,time=None):
		""" Check and Process Arguments """

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
		""" Update UI with results """
		
		self.palette = [
			('body','dark cyan', '', 'standout'),
			('focus','dark red', '', 'standout'),
			('head','light red', 'black'),
		]

		self.videolist = []
		for entry in feed.entry:
			
			try:
				self.videolist.append(ItemWidget(entry))
			
			except Exception as e: 
				print('search failed:\nError: %s' % e)

		self.listbox = urwid.ListBox(urwid.SimpleListWalker(self.videolist))
		self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'))
		self.loop = urwid.MainLoop(self.view, self.palette, unhandled_input=self.keystroke)
		self.loop.run()


	def download(self, entry):
		""" Download one video """
		
		try:
			download.main(entry)
		except Exception as e:
			print('download failed:\nError: %s' % e)


	def downloadFeed(self,feed):
		""" Download multiple video's """

		for entry in feed.entry:
			try:
				download.main(entry.media.player.url)
			except Exception as e:
				print('download failed:\nError: %s' % e)



	def stream(self, entry):
		""" Stream one video """

		urls = []
		try:
			stream.main(entry)
		except stream.ReturnUrl as url:
			urls.append(str(url))
		except Exception as e:
			print('download failed:\nError: %s' % e)
		player = YoutubePlayer(urls)
		

	def streamFeed(self,feed):
		""" Stream multiple video's """
		
		urls = []
		for entry in feed.entry:
			try:
				stream.main(entry.media.player.url)
			except stream.ReturnUrl as url:
				print '[youtube] Found location for video %s' %entry.title.text
				print '[youtube] URL: %s' %url
				urls.append(str(url))
			except Exception as e:
				print('download failed:\nError: %s' % e)
		player = YoutubePlayer(urls)


	def execute(self):
		""" Execute query and handle results """

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
		if command == 'download': self.downloadFeed(feed)
		if command == 'stream':	self.streamFeed(feed)
		if command == 'search':	self.search(feed)


	def keystroke (self,input):
		""" Handle Keystrokes """
		
		if input in ('q', 'Q'):
			raise urwid.ExitMainLoop()

		if input is 'enter':
			try:
				self.focus = self.listbox.get_focus()[0].content
			except Exception as e:
				print('listbox get_focus failed:\nError: %s' % e)
			self.stream(self.focus)

		if input is ' ':
			try:
				self.focus = self.listbox.get_focus()[0].content
			except Exception as e:
				print('listbox get_focus failed:\nError: %s' % e)
			self.download(self.focus)


			

if len(sys.argv) == 7:
	YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
if len(sys.argv) == 6:
	if sys.argv[5] == 'shuffle': YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], None)
	else: YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], None, sys.argv[5])
if len(sys.argv) == 5:
	YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])