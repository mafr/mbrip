import sys
from musicbrainz2.disc import getSubmissionUrl
from mbrip.ui import Menu, queryUser, parseSpan
from mbrip.webservice import readDisc, getMatchingReleases, loadRelease
from mbrip.todo import createTodoList
from mbrip.utils import errQuit
from mbrip.coverdownloader import download_cover
import mbrip.ripper
import mbrip.encoder
import mbrip.tagger


class State:
	SELECT_RELEASE = 1
	SHOW_RELEASE = 2
	SELECT_TRACKS = 3
	RIP_TRACKS = 4
	QUIT = 5

class Controller:
	"""A state machine for handling user interaction.

	Each state represents one screen. We associate a handler function
	with each state which implements the transition to the next state
	based on user input.
	"""

	def __init__(self, fileNameFormatter, ripper, encoder, tagger,
            preselectedReleaseId=None):
		self.preselectedReleaseId = preselectedReleaseId
		self.releaseToRip = None
		self.stateTable = {
			State.SELECT_RELEASE: self.selectReleaseHandler,
			State.SHOW_RELEASE: self.showReleaseHandler,
			State.SELECT_TRACKS: self.selectTracksHandler,
			State.RIP_TRACKS: self.ripTracksHandler,
		}
		self.fileNameFormatter = fileNameFormatter
		self.ripper = ripper
		self.encoder = encoder
		self.tagger = tagger

	def run(self):
		state = State.SELECT_RELEASE
		while state != State.QUIT:
			handler = self.stateTable[state]
			state = handler()
			

	def selectReleaseHandler(self):
		if self.preselectedReleaseId:
			disc = None
			results = [ loadRelease(self.preselectedReleaseId) ]
		else:
			disc = readDisc()
			results = getMatchingReleases(disc)

			if len(results) == 0:
				errQuit("no disc found")

		menu = Menu('1', 'Please select a release to rip:')

		for i, r in enumerate(results, 1):
			label = '%s - %s [%s]' % (r.artist.name, r.title,
				', '.join([e.country + ' ' + e.date for e in r.releaseEvents]))
			menu.addChoice(str(i), label)

		menu.addChoice(None, None)
		if disc:
			menu.addChoice('n', 'None of those, show submission URL.')
		menu.addChoice('q', 'Quit')

		choice = menu.showMenu()

		if choice == 'q':
			return State.QUIT
		elif disc and choice == 'n':
			print
			print "Use this URL to submit the disc to MusicBrainz:"
			print " ", getSubmissionUrl(disc)
			return State.QUIT
		else:
			self.releaseToRip = results[int(choice)-1]
			return State.SHOW_RELEASE

		assert( False )


	def showReleaseHandler(self):
		print "loading release from server ... "
		print

		release = loadRelease(self.releaseToRip.id)
		self.releaseToRip = release

		# Now display the returned data.
		#
		isSingleArtist = release.isSingleArtistRelease()

		print "%s - %s" % (
			release.artist.getUniqueName(), release.title)

		for i, t in enumerate(release.tracks, 1):
			if isSingleArtist:
				title = t.title
			else:
				trackArtist = t.artist if t.artist else release.artist
				title = trackArtist.name + ' - ' +  t.title

			(min, sec) = t.getDurationSplit()
			print " %2d. %s (%d:%02d)" % (i, title, min, sec)


		menu = Menu('r', 'Please select:')
		menu.addChoice('r', 'Rip all tracks')
		menu.addChoice('s', 'Select the tracks to rip')
		menu.addChoice('b', 'Back to release selection')
		menu.addChoice('q', 'Quit')

		choice = menu.showMenu()

		if choice == 'r':
			print 'Ripping all tracks ...'
			self.tracksToRip = range(1, len(release.tracks)+1)
			return State.RIP_TRACKS
		elif choice == 's':
			return State.SELECT_TRACKS
		elif choice == 'b':
			return State.SELECT_RELEASE
		elif choice == 'q':
			return State.QUIT

		assert( False )


	def selectTracksHandler(self):
		print "Which tracks should be ripped?"

		default = '%d-%d' % (1, len(self.releaseToRip.tracks))
		prompt = 'select (default: %s) > ' % default
		value = queryUser(prompt, default)

		self.tracksToRip = parseSpan(value)

		return State.RIP_TRACKS


	def ripTracksHandler(self):
		download_cover(self.releaseToRip)

		todo = createTodoList(self.releaseToRip, self.tracksToRip,
			self.fileNameFormatter)

		self.ripper.ripTracks(todo)
		self.encoder.encodeTracks(todo, self.tagger)

		return State.QUIT


# EOF
