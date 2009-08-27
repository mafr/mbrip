#! /usr/bin/env python
import sys
from mbrip.controller import Controller
from mbrip.ripper import CdParanoia
from mbrip.encoder import Lame
from mbrip.formatter import Formatter
from mbrip.tagger import EyeD3
from mbrip.utils import errQuit


#
# Configuration.
#
ripper = CdParanoia('/usr/bin/cdparanoia')

encoder = Lame('/usr/bin/lame', '--r3mix')

fileNameFormatter = Formatter(
	pattern='${num} - ${artist} - ${title}',
	whitelist=None,
	rewriteMap={ '/': '', '\\': '' },
)

tagger = EyeD3()


# Nothing to change from here on.
#

ctrl = Controller(
	fileNameFormatter=fileNameFormatter,
	ripper=ripper, encoder=encoder, tagger=tagger,
)

try:
	ctrl.run()
except KeyboardInterrupt:
	errQuit("\nInterrupted on by user. Exiting.")

# EOF
