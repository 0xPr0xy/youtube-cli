import urwid
import vlc


class YoutubePlayer:
	

	def __init__(self, playlist):
		
		self.palette = [
			('banner', '', '', '', '#fff', '#333'),
			('streak', '', '', '', '#fff', '#333'),
			('bg', '', '', '', '', '#666'),]

		txt = urwid.Text(('banner', u"0xPr0xy Youtube Player! v0.2"), align='center')
		map1 = urwid.AttrMap(txt, 'streak')
		fill = urwid.Filler(map1)
		self.map2 = urwid.AttrMap(fill, 'bg')
		self.create_player(playlist)


	def handle_input(self,input):
		
		if input in ('q', 'Q'):
			self.player.stop()
			raise urwid.ExitMainLoop()
		if input in ('p', 'P'):
			self.player.pause()
		if input in ('r', 'R'):
			self.player.restart()
		if input in (']','}'):
			self.player.next()
		if input in ('{', '['):
			self.player.previous()

	
	def create_player(self, playlist):
		instanceParameters = [
			'--quiet',
			'--ignore-config',
			'--sout-keep',
			'--sout-all',
		]
		self.instance=vlc.Instance(instanceParameters)
		self.medialist = self.instance.media_list_new()
		for item in playlist:
			self.medialist.add_media(self.instance.media_new(item))
		self.player = self.instance.media_list_player_new()
		self.player.set_media_list(self.medialist)
		self.loop = urwid.MainLoop(self.map2, self.palette, unhandled_input=self.handle_input)
		self.loop.screen.set_terminal_properties(colors=256)
		self.player.play()
		self.loop.run()