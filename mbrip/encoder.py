import sys
import os
import os.path

class Lame:
	path = '/usr/bin/lame'

	def __init__(self, path=None):
		self.path = path or self.path
		if not os.path.exists(self.path):
			print "Error: Binary %s does not exist." % self.path
			sys.exit(2)

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
			ret = os.spawnl(os.P_WAIT, self.path,
				'lame', wavfile, tmpfile)

			if ret != 0:
				print "error executing lame"
				sys.exit(1)

			tagger.tagTrack(todoEntry)

			os.rename(tmpfile, mp3file)
			os.unlink(wavfile)

		except KeyboardInterrupt:
			print
			print "cancelled on user request"
			os.unlink(tmpfile)
			sys.exit(1)

# EOF
