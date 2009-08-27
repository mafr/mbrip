import sys
import os
import os.path

from mbrip.utils import errQuit


class CdParanoia:
	PATH = '/usr/bin/cdparanoia'

	def __init__(self, path=PATH):
		self.path = path
		if not os.path.exists(self.path):
			errQuit("Error: Binary %s does not exist." % self.path)


	def ripTracks(self, todoList):
		for entry in todoList:
			self.ripTrack(entry)

	def ripTrack(self, todoEntry):
		wavfile = todoEntry['wavfile']
		mp3file = todoEntry['mp3file']
		tmpfile = wavfile + '.tmp'

		if os.path.exists(wavfile) or os.path.exists(mp3file):
			print "Track %s has already been ripped. Skipping." % todoEntry['num']
			return

		try:
			ret = os.spawnl(os.P_WAIT, self.path,
				'cdparanoia', str(todoEntry['num']), tmpfile)

			if ret != 0:
				errQuit("error executing cdparanoia")

			os.rename(tmpfile, wavfile)

		except KeyboardInterrupt:
			os.unlink(tmpfile)
			errQuit("\ncancelled on user request")


# EOF
