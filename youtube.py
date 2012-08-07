#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import random
import logging

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


class CustomEdit(urwid.Edit):

	__metaclass__ = urwid.signals.MetaSignals
	signals = ['done']

	def keypress(self, size, key):

		if key == 'enter':
			urwid.emit_signal(self, 'done', self.get_edit_text())
			return

		elif key == 'esc':
			urwid.emit_signal(self, 'done', None)
			return

		urwid.Edit.keypress(self, size, key)




class ItemWidget (urwid.WidgetWrap):

	def __init__ (self, item, entry=None):

		try:

			logging.basicConfig(filename='.youtube-cli.log',level=logging.DEBUG)
			
			if item == 'content' and entry:

				self.content = entry.media.player.url
				title = ('weight', 3, urwid.Padding(urwid.AttrWrap(
				urwid.Text('%s' % ( entry.title.text)),  'body', 'focus')))
				rating = ('weight', 1, urwid.Padding(urwid.AttrWrap(
				urwid.Text('Rating:%s' % ( entry.rating.average)),  'body')))
				viewcount = ('weight', 1, urwid.Padding(urwid.AttrWrap(
				urwid.Text('Viewcount:%s' % ( entry.statistics.view_count )),  'body')))
				item = [title, rating, viewcount]
				content = urwid.Columns(item)
				self.__super.__init__(content)
			
			elif item == 'header':

				title = ('weight', 3, urwid.Padding(urwid.AttrWrap(
				urwid.Text('Title'),  'header', 'focus')))
				rating = ('weight', 1, urwid.Padding(urwid.AttrWrap(
				urwid.Text('Rating'),  'header', 'focus')))
				viewcount = ('weight', 1, urwid.Padding(urwid.AttrWrap(
				urwid.Text('Viewcount'),  'header', 'focus')))
				item = [title, rating, viewcount]
				header = urwid.Columns(item)
				self.__super.__init__(header)

		except Exception as e:
			logging.exception(e)

	def selectable (self):
		return True

	def keypress(self, size, key):
		return key




class YoutubeClient:

	def __init__(self,keyword,q,order,num_results,shuffle=None,time=None):

		try:

			logging.basicConfig(filename='.youtube-cli.log',level=logging.DEBUG)
			
			keywords = ['search', 'download', 'stream']

			if keyword in keywords: 
				self.keyword = keyword
			else: 
				sys.exit('invalid keyword')

			self.q = q
			ordering_key = {'rating':'rating', 'viewcount':'viewCount','relevance':'relevance','published':'published'}
			ordering = ['rating','viewcount','relevance']

			if order in ordering: 
				self.order = ordering_key[order]
			else: 
				sys.exit('invalid ordering')

			try: 
				self.num = int(num_results)
			except Exception as e: 
				sys.exit('invalid number %s' %e)

			if shuffle is not None: 
				self.shuffle = shuffle
			else: 
				self.shuffle = False

			times_key = {'today':'today','week':'this_week','month':'this_month','time':'all_time'}
			times = ['today', 'this_week', 'this_month', 'all_time']

			if time is not None and time in times: 
				self.time = times_key[time]
			else: 
				self.time = False

		except Exception as e:
			logging.exception(e)

		self.execute()


	def search(self,feed):

		try:
			self.palette = [
					('body','dark cyan', '', 'standout'),
					('focus'
						,'dark red', '', 'standout'),
					('header','dark red', '', 'standout'),
			]
			self.videolist = []
			self.videolist.append(ItemWidget('header'))

			for entry in feed.entry:
				self.videolist.append(ItemWidget('content', entry))

			self.listbox = urwid.ListBox(urwid.SimpleListWalker(self.videolist))
			self.view = urwid.Frame(urwid.AttrWrap(self.listbox, 'body'))
			self.loop = urwid.MainLoop(self.view, self.palette, unhandled_input=self.keystroke)
			self.loop.run()

		except Exception as e:
			logging.exception(e)



	def download(self, entry):

		try:
			download.main(entry)

		except Exception as e:
			logging.exception(e)


	def downloadFeed(self,feed):

		try:
			for entry in feed.entry:
				download.main(entry.media.player.url)

		except Exception as e:
			logging.exception(e)



	def stream(self, entry):

		urls = []
		try:
			stream.main(entry)

		except stream.ReturnUrl as url:
			urls.append(str(url))

		except Exception as e:
			logging.exception(e)

		player = YoutubePlayer(urls)


	def streamFeed(self,feed):

		urls = []
		try:
			for entry in feed.entry:
				stream.main(entry.media.player.url)

		except stream.ReturnUrl as url:
			urls.append(str(url))

		except Exception as e:
			logging.exception(e)

		player = YoutubePlayer(urls)


	def execute(self):

		try:
			
			self.client = gdata.youtube.service.YouTubeService()
			query = gdata.youtube.service.YouTubeVideoQuery()
			query.format = '5'
			query.hd = True
			query.vq = self.q
			query.max_results = self.num
			query.start_index = 1
			query.racy = 'exclude'
			query.orderby = self.order

			if self.time: 
				query.time = self.time

			feed = self.client.YouTubeQuery(query)

			if self.shuffle: 
				random.shuffle(feed.entry)

			command = self.keyword

			if command == 'download': 
				self.downloadFeed(feed)
			
			if command == 'stream': 
				self.streamFeed(feed)
			
			if command == 'search': 
				self.search(feed)

		except Exception as e:
			logging.exception(e)


	def keystroke (self,input):

		if input in ('e', 'E'):

			try:
				self.edit()

			except Exception as e:
				logging.exception(e)


		if input is 'enter':

			try:
				self.focus = self.listbox.get_focus()[0].content
				self.stream(self.focus)

			except Exception as e:
				logging.exception(e)


		if input is ' ':
			
			try:
				self.focus = self.listbox.get_focus()[0].content
				self.download(self.focus)

			except Exception as e:
				logging.exception(e)

		if input in ('q', 'Q'):

			raise urwid.ExitMainLoop()


	def edit(self):

		try:
			self.foot = CustomEdit('search: ')
			self.footer = urwid.AttrWrap(self.foot, 'header', 'focus')
			self.view.set_footer(self.footer)
			self.view.set_focus('footer')
			urwid.connect_signal(self.foot, 'done', self.edit_done)
		
		except Exception as e:
			logging.exception(e)


	def edit_done(self, content):
		
		try:
			self.view.set_focus('body')
			urwid.disconnect_signal(self, self.foot, 'done', self.edit_done)
			
			if content:
				self.q = '\"'+content+'\"'
				self.num = 50
				self.order = 'relevance'
				self.execute()
			
			self.view.set_footer(None)
		
		except Exception as e:
			logging.exception(e)


if len(sys.argv) == 7:
	YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

if len(sys.argv) == 6:
	if sys.argv[5] == 'shuffle': YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], None)
	else: YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], None, sys.argv[5])

if len(sys.argv) == 5:
	YoutubeClient(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
