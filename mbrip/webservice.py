import sys
import musicbrainz2.disc as mbdisc
import musicbrainz2.webservice as mbws

def readDisc():
	try:
		return mbdisc.readDisc()
	except mbdisc.DiscError, e:
		print "Error:", e
		sys.exit(1)


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
		print "Error:", e
		sys.exit(2)

	return results


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
		print "Error:", e
		sys.exit(2)

	return release

# EOF
