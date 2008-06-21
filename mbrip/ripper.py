import sys
import os
import os.path


class CdParanoia:
	path = '/usr/bin/cdparanoia'

	def __init__(self):
		if not os.path.exists(self.path):
			print "Error: Binary %s does not exist." % self.path
			sys.exit(2)

	def ripTracks(self, todoList):
		for entry in todoList:
			self.ripTrack(entry)

	def ripTrack(self, todoEntry):
		wavfile = todoEntry['wavfile']
		mp3file = todoEntry['mp3file']
		tmpfile = wavfile + '.tmp'

		if os.path.exists(wavfile) or os.path.exists(mp3file):
			print "not ripping track %d again" % todoEntry['num']
			return

		try:
			ret = os.spawnl(os.P_WAIT, self.path,
				'cdparanoia', str(todoEntry['num']), tmpfile)

			if ret != 0:
				print "error executing cdparanoia"
				sys.exit(1)

			os.rename(tmpfile, wavfile)

		except KeyboardInterrupt:
			print
			print "cancelled on user request"
			os.unlink(tmpfile)
			sys.exit(1)


# EOF
