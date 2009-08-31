"""Various assorted utility functions."""
import sys

def errLog(msg):
	print >>sys.stderr, msg

def errQuit(message):
	print >>sys.stderr, msg
	sys.exit(1)

class Error(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return self.msg

class RecoverableError(Error):
	pass

class FatalError(Error):
	pass

# EOF
