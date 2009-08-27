mbrip - A MusicBrainz-Powered Command Line Audio CD Ripper
----------------------------------------------------------

This is a pre-alpha version of a MusicBrainz based command line CD ripper
written by Matthias Friedrich <matt@mafr.de>.

There are two ways to run it: The first one works without installing the
package. Put a CD into your default disc drive and run the following command:

  $ PYTHONPATH=. python bin/mbrip

The second one is to install it using setup.py:

  # python setup.py install

Note that on Debian-based systems like Ubuntu, you have to add the
--install-layout=deb command line switch or it won't work on Python 2.6
and later.

After that, you can run the program using this command:

  $ mbrip

EOF
