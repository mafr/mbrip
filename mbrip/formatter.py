import string
import re


#
# TODO:
#  * provide a hook to post/preprocess path components
#
class Formatter(object):
	"""Format a file name.

	This formatter basically consists of two parts:

	  1. Remove all characters which are not in the whitelist.
	  2. Rewrite the characters in the string based on a rewrite map.
	"""
	def __init__(self, pattern, whitelist=None, rewriteMap={ }):
		self._pattern = pattern
		self._whitelist = whitelist
		self._rewriteMap = rewriteMap

	def _applyWhitelist(self, name):
		if self._whitelist is None:
			return name
		else:
			return (x for x in name if x in self._whitelist)

	def _rewriteChars(self, name):
		return (self._rewriteMap.get(x, x) for x in name)

	def _sanitize(self, name):
		if name is None:
			return ''
		return ''.join(self._rewriteChars(self._applyWhitelist(name)))

	def format(self, metaDict):
		d = { k:self._sanitize(v) for k, v in metaDict.items() }
		return string.Template(self._pattern).substitute(d)


class ShellFriendlyFormatter(Formatter):
	"""Like Formatter, but with shell-friendly whitelist and rewrite map."""

	WHITELIST = { x for x in ' -._' + string.letters + string.digits }
	REWRITE_MAP = { ' ': '_', '/': '' }

	def __init__(self, pattern, whitelist=WHITELIST, rewriteMap=REWRITE_MAP):
		super(ShellFriendlyFormatter, self).__init__(
			pattern, whitelist, rewriteMap)


if __name__ == '__main__':
	metaDict = {
		'num': '%02d' % 7,
		'artist': 'Tori Amos',
		'title': 'Tear in Your Hand',
	}

	f = ShellFriendlyFormatter('${num} - ${artist} - ${title}')

	print f.format(metaDict)

# EOF
