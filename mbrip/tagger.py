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


ENC_UTF8 = 3

class MutagenId3:
	def __init__(self):
		try:
			import mutagen.id3 as id3
		except ImportError:
			errQuit("Error: package eyeD3 not found.")

	def tagTrack(self, todoEntry):
		fileName = todoEntry['mp3file'] + '.tmp'
		release = todoEntry['release']
		track = todoEntry['track']
		trackNum = todoEntry['num']

		audio = id3.ID3(fileName)

		if track.artist is None:
			audio.add(id3.TPE1(encoding=ENC_UTF8, text=release.artist.name))
		else:
			audio.add(id3.TPE1(encoding=ENC_UTF8, text=track.artist.name))

		audio.add(id3.TIT2(encoding=ENC_UTF8, text=track.title))
		audio.add(id3.TALB(encoding=ENC_UTF8, text=release.title))
		#audio.add(id3.TRCK(text='%d/%d' % (trackNum, len(release.tracks))))
		audio.add(id3.TRCK(text='%d' % (trackNum, )))

		audio.save()


if __name__ == '__main__':
	from musicbrainz2.model import Artist, Release, Track

	artist = Artist(name=u'Tori Amos')
	release = Release(title=u'Little Earthquakes')
	release.artist = artist
	track = Track(title='Tear In Your Hand')

	todoEntry = {
		'num':		7,
		'mp3file':	'Tear_In_Your_Hand.mp3',
		'release':	release,
		'track':	track,
	}

	m = MutagenId3()
	m.tagTrack(todoEntry)

# EOF
