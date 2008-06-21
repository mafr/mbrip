import sys
from mbrip.utils import errQuit

from musicbrainz2.utils import extractUuid, extractFragment
from musicbrainz2.model import NS_MMD_1


# Keys for the UFID and TXXX frames
#
FILE_ID = 'http://musicbrainz.org'
ARTIST_ID = 'MusicBrainz Artist Id'
ALBUM_ID = 'MusicBrainz Album Id'
ALBUM_ARTIST = 'MusicBrainz Album Artist'
ALBUM_ARTIST_SORTNAME = 'MusicBrainz Album Artist Sortname'
ALBUM_ARTIST_ID = 'MusicBrainz Album Artist Id'
ALBUM_STATUS = 'MusicBrainz Album Status'
ALBUM_TYPE = 'MusicBrainz Album Type'
RELEASE_COUNTRY = 'MusicBrainz Album Release Country'


class EyeD3:
	def __init__(self):
		try:
			import eyeD3
		except ImportError:
			errQuit("Error: package eyeD3 not found.")

	def tagTrack(self, todoEntry):
		import eyeD3

		fileName = todoEntry['mp3file'] + '.tmp'
		release = todoEntry['release']
		track = todoEntry['track']

		tag = eyeD3.Tag()
		tag.link(str(fileName)) # eyeD3 doesn't like unicode strings
		tag.header.setVersion(eyeD3.ID3_V2)

		if track.artist is None:
			tag.setArtist(release.artist.name)
		else:
			tag.setArtist(track.artist.name)

		tag.setTitle(track.title)
		tag.setAlbum(release.title)
		tag.setTrackNum( (todoEntry['num'], len(release.tracks)) )

		types = (release.TYPE_OFFICIAL, release.TYPE_PROMOTION,
			release.TYPE_BOOTLEG)

		for t in release.types:
			value = extractFragment(t, NS_MMD_1)
			if t in types:
				tag.addUserTextFrame(ALBUM_TYPE, value)
			else:
				tag.addUserTextFrame(ALBUM_STATUS, value)

		tag.addUserTextFrame(ALBUM_ARTIST, release.artist.name)
		tag.addUserTextFrame(ALBUM_ARTIST_SORTNAME,
			release.artist.sortName)

		tag.addUniqueFileID(FILE_ID, str(extractUuid(track.id)))

		if track.artist is None:
			tag.addUserTextFrame(ARTIST_ID,
				extractUuid(release.artist.id))
		else:
			tag.addUserTextFrame(ARTIST_ID, extractUuid(artist.id))

		tag.addUserTextFrame(ALBUM_ID, extractUuid(release.id))
		tag.addUserTextFrame(ALBUM_ARTIST_ID,
			extractUuid(release.artist.id))

		event = release.getEarliestReleaseEvent()
		if event is not None:
			tag.addUserTextFrame(RELEASE_COUNTRY, event.country)
			tag.setDate(event.date[0:4])

		tag.update(eyeD3.ID3_V2_3)

# EOF
