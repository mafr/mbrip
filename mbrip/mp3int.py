#! /usr/bin/env python
import sys
import os
import optparse
import mutagen.id3 as mid3


repositoryRoot = '/tmp'



def integrate_file(srcfile, opts):
	print 'Creating TODO (from %s) ...' % (srcfile, )

	print opts.move

	# 1. Open and read tag. exit if no tag or tag incomplete.
	# 2. Work out file type (album, maxi, etc.). How?
	# 3. Create a file name using mbrip's ShellFriendlyFormatter

	# TODO: obviously
	filename = 'Tori_Amos/albums/Whatever.mp3'

	# 4. Figure out target filename
	destfile = os.path.join(opts.root_dir, filename)

	# 5. Create the target directory
	destdir = os.path.dirname(destfile)
	os.makedirs(destdir)

	# 6. Copy/move the file there if it doesn't exist yet

	# 7. Set integration date??
	# 8. Fix permissions??
	pass


def integrate_files(filenames, opts):
	for f in filenames:
		integrate_file(f, opts)



op = optparse.OptionParser('usage: %prog [options] filenames...')

op.add_option('-r', '--root-dir', default='',
	help="Files are generated relative to this (default: '')", metavar="DIR")
op.add_option('-m', '--move', action='store_true',
	help="Move the file, don't copy")
op.add_option('-f', '--force', action='store_true',
	help='Overwrite existing files')
op.add_option('-q', '--quiet', action='store_true',
	help='No status output')

opts, args = op.parse_args()


try:
	integrate_files(args, opts)
#except SomeError, e:
#	pass
except KeyboardInterrupt:
	pass


filename = 'Tori_Amos/albums/Whatever.mp3'

destfile = os.path.join(repositoryRoot, filename)
destdir = os.path.dirname(destfile)

if os.path.exists(destfile):
	print 'error: file already exists'
	sys.exit(1)

if not os.path.isdir(destdir):
	print 'creating', destdir
	os.makedirs(destdir)


print destfile
print destdir
