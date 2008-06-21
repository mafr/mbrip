import sys

def createMetaDict(trackNum, release, track):
	artist = track.artist or release.artist
	return {
		'num':		'%02d' % trackNum,
		'artist':	artist.name,
		'title':	track.title,
	}


def createTodoList(release, trackList, fileNameFormatter):
	todo = [ ]
	for i in trackList:
		track = release.tracks[i-1]

		try:
			metaDict = createMetaDict(i, release, track)
			fileBase = fileNameFormatter.format(metaDict)
		except KeyError, e:
			print "Error: invalid key in file name pattern:", e
			sys.exit(1)

		entry = {
			'num':		i,
			'wavfile':	fileBase + '.wav',
			'mp3file':	fileBase + '.mp3',
			'release':	release,
			'track':	track,
		}
		todo.append(entry)

	return todo

