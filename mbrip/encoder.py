import sys
import os
import os.path

from mbrip.utils import errQuit


class Lame:
	"""A lame-based MP3 encoder."""

	PATH = '/usr/bin/lame'

	def __init__(self, path=PATH, *args):
		self.path = path
		self.args = args
		if not os.path.exists(self.path):
			errQuit("Error: Binary %s does not exist." % self.path)


	def encodeTracks(self, todoList, tagger):
		for entry in todoList:
			self.encodeTrack(entry, tagger)


	def encodeTrack(self, todoEntry, tagger):
		wavfile = todoEntry['wavfile']
		mp3file = todoEntry['mp3file']
		tmpfile = mp3file + '.tmp'

		if os.path.exists(mp3file):
			print "not encoding track %d again" % todoEntry['num']
			return


		try:
			args = [os.P_WAIT, self.path, 'lame']
			args += self.args
			args += [wavfile, tmpfile]

			ret = os.spawnl(*args)

			if ret != 0:
				errQuit("error executing lame")

			tagger.tagTrack(todoEntry)

			os.rename(tmpfile, mp3file)
			os.unlink(wavfile)

		except KeyboardInterrupt:
			os.unlink(tmpfile)
			print
			errQuit("\ncancelled on user request")

# EOF
