import sys
from mbrip.utils import errQuit

try:
	import musicbrainz2.disc as mbdisc
	import musicbrainz2.webservice as mbws
except ImportError:
	errQuit("Error: Please install the python-musicbrainz2 package.")


def readDisc():
	try:
		return mbdisc.readDisc()
	except mbdisc.DiscError, e:
		errQuit("Error: Cannot read disc: " + str(e))


def getMatchingReleases(disc):
	# Setup a Query object.
	#
	service = mbws.WebService()
	query = mbws.Query(service)

	# Query for all discs matching the given DiscID.
	#
	try:
		filter = mbws.ReleaseFilter(discId=disc.id)
		results = query.getReleases(filter)
	except mbws.WebServiceError, e:
		errQuit("Error: " + str(e))

	return [r.release for r in results]


def loadRelease(releaseId):
	# Setup a Query object.
	#
	service = mbws.WebService()
	query = mbws.Query(service)

	try:
		inc = mbws.ReleaseIncludes(artist=True, tracks=True,
			releaseEvents=True)
		release = query.getReleaseById(releaseId, inc)
	except mbws.WebServiceError, e:
		errQuit("Error: " + str(e))

	return release

# EOF
