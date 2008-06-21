#! /usr/bin/env python
import sys
import mbrip.controller as controller
import mbrip.formatter
import mbrip.ripper
import mbrip.encoder
import mbrip.tagger


#
# Configuration.
#
ripper = mbrip.ripper.CdParanoia('/usr/bin/cdparanoia')

encoder = mbrip.encoder.Lame('/usr/bin/lame')

fileNameFormatter = mbrip.formatter.Formatter(
	pattern='${num} - ${artist} - ${title}',
	whitelist=None,
	rewriteMap={ '/': '', '\\': '' },
)

tagger = mbrip.tagger.EyeD3()


# Nothing to change from here on.
#

try:
	import musicbrainz2
except:
	print "Error: please install the python-musicbrainz2 package."
	sys.exit(1)


ctrl = controller.Controller(
	fileNameFormatter=fileNameFormatter,
	ripper=ripper, encoder=encoder, tagger=tagger,
)

ctrl.run()
