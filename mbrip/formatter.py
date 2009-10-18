import string
import re


#
# TODO:
#  * provide a hook to post/preprocess path components
#  * prefix applyWhitelist etc. with underscore to mark them as private
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

	def applyWhitelist(self, name, whitelist):
		"""Return the input string, only keeping the allowed chars."""
		allowed = dict( map(lambda x: (x, True), whitelist) )

		tmp = ''
		for c in name:
			if c in allowed:
				tmp += c

		return tmp


	def rewriteChars(self, name, rewriteMap={ }):
		tmp = ''
		for c in name:
			tmp += rewriteMap.get(c, c)
		return tmp


	def rewritePathComponent(self, name):
		if name is None:
			return ''

		if self._whitelist is not None:
			name = self.applyWhitelist(name, self._whitelist)

		name = self.rewriteChars(name, self._rewriteMap)

		return name

	def format(self, metaDict):
		# We don't want to modify metaDict, so we work on a copy.
		d = dict(metaDict)
		for key in d:
			d[key] = self.rewritePathComponent(d[key])

		return string.Template(self._pattern).substitute(d)


class ShellFriendlyFormatter(Formatter):
	"""Like Formatter, but with shell-friendly whitelist and rewrite map."""

	WHITELIST = ' -._' + string.letters + string.digits
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
