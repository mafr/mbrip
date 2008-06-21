

def createTodoList(release, trackList):
	todo = [ ]
	for i in trackList:
		track = release.tracks[i-1]

		entry = {
			'num':		i,
			'wavfile':	'%02d - %s.wav' % (i, track.title),
			'mp3file':	'%02d - %s.mp3' % (i, track.title),
			'release':	release,
			'track':	track,
		}
		todo.append(entry)

	return todo

