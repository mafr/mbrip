#! /usr/bin/env python
import sys
import mbrip.controller as controller
import mbrip.ripper as ripper
import mbrip.encoder as encoder
import mbrip.tagger as tagger

try:
	import musicbrainz2
except:
	print "Error: please install the python-musicbrainz2 package."
	sys.exit(1)


ctrl = controller.Controller(
	ripper=ripper.CdParanoia(),
	encoder=encoder.Lame(),
	tagger=tagger.EyeD3(),
)

ctrl.run()
