import os
import shutil
import mutagen.id3 as mid3
from mbrip.utils import RecoverableError, FatalError, errLog
from mbrip.metadata import Id3Tag
from mbrip.formatter import ShellFriendlyFormatter


def integrate_files(filenames, opts):
	for f in filenames:
		try:
			integrate_file(f, opts)
		except RecoverableError as e:
			errLog(str(e))


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
	try:
		tag = Id3Tag()
		tag.load(srcfile)

		# 2. Work out file type (album, maxi, etc.). How?
		return tag
	except IOError as e:
		raise RecoverableError(
			'Cannot read file %s: %s' % (e.filename, e.strerror))


def build_filename(srcfile, metadata, opts):
	root, ext = os.path.splitext(srcfile)

	# TODO 3: pattern should be in opts!
	formatter = ShellFriendlyFormatter('${artist}/${track}_${title}')
	filename = formatter.format(metadata) + ext

	return os.path.join(opts.root_dir, filename)


def create_dir_for_file(filename):
	destdir = os.path.dirname(filename)

	if not os.path.exists(destdir):
		try:
				os.makedirs(destdir)
		except (IOError, OSError) as e:
				raise RecoverableError(
					'Cannot create directory %s: %s' % (destdir, e.strerror))


def copy_or_move(srcfile, destfile, opts):
	if os.path.exists(destfile) and not opts.force:
		raise RecoverableError(
			'Skipping, file %s already exists' % (destfile, ))

	if not opts.quiet:
		print 'Creating %s ...' % (destfile, )

	try:
			if opts.move:
				shutil.move(srcfile, destfile)
			else:
				shutil.copy(srcfile, destfile)
	except (OSError, IOError) as e:
		raise RecoverableError(
			'Cannot create file %s: %s' % (destfile, e.strerror))

# EOF
