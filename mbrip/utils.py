"""Various assorted utility functions."""
import sys

def errQuit(msg):
	print >>sys.stderr, msg
	sys.exit(1)

# EOF
