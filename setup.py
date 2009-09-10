#! /usr/bin/env python
from distutils.core import setup
import mbrip

setup_args = {
	'name':		'mbrip',
	'version':	mbrip.__version__,
	'description':	'A MusicBrainz-Powered Command Line Audio CD Ripper',
	'author':	'Matthias Friedrich',
	'author_email':	'matt@mafr.de',
	'url':		'http://mafr.de/',
	'license':	'GPL',
	'packages':	[ 'mbrip' ],
	'scripts':	[ 'bin/mbrip', 'bin/mp3int' ],
}

setup(**setup_args)

# EOF
