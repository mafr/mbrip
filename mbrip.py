#! /usr/bin/env python
import sys
import mbrip.controller as controller
import mbrip.ripper
import mbrip.encoder 
import mbrip.tagger

from mbrip.formatter import Formatter
from mbrip.utils import errQuit


#
# Configuration.
#
ripper = mbrip.ripper.CdParanoia('/usr/bin/cdparanoia')

encoder = mbrip.encoder.Lame('/usr/bin/lame', '--r3mix')

fileNameFormatter = Formatter(
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
	errQuit("Error: please install the python-musicbrainz2 package.")


ctrl = controller.Controller(
	fileNameFormatter=fileNameFormatter,
	ripper=ripper, encoder=encoder, tagger=tagger,
)

ctrl.run()

# EOF
