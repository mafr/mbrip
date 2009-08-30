import os
import shutil
import mutagen.id3 as mid3
from mbrip.formatter import ShellFriendlyFormatter


def integrate_files(filenames, opts):
	for f in filenames:
		integrate_file(f, opts)


def integrate_file(srcfile, opts):
	metadata = load_metadata(srcfile)

	destfile = build_filename(srcfile, metadata, opts)

	create_dir_for_file(destfile)

	copy_or_move(srcfile, destfile, opts)

	# TODO 2
	# 7. Set integration date??
	# 8. Fix permissions??


def load_metadata(srcfile):
	# TODO 1
	# 1. Open and read tag. exit if no tag or tag incomplete.
	# 2. Work out file type (album, maxi, etc.). How?

	return { 'artist': 'Tori Amos', 'title': 'Tear in Your Hand' }


def build_filename(srcfile, metadata, opts):
	root, ext = os.path.splitext(srcfile)

	formatter = ShellFriendlyFormatter('${artist}/${title}')
	filename = formatter.format(metadata) + ext

	return os.path.join(opts.root_dir, filename)


def create_dir_for_file(filename):
	destdir = os.path.dirname(filename)

	if not os.path.exists(destdir):
		os.makedirs(destdir)


def copy_or_move(srcfile, destfile, opts):
	if os.path.exists(destfile) and not opts.force:
		print 'Skipping, file %s already exists' % (destfile, )
		return

	if not opts.quiet:
		print 'Creating %s ...' % (destfile, )

	if opts.move:
		shutil.move(srcfile, destfile)
	else:
		shutil.copy(srcfile, destfile)

# EOF
