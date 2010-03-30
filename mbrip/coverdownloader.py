"""Amazon-related functionality.

Mostly creating URLs to Amazon based on ASINs.
"""

import urllib

IMAGE_SIZE_LARGE = '_SL500_'
IMAGE_SIZE_MEDIUM = '._SL160_'
IMAGE_SIZE_SMALL = '._SL110_'
IMAGE_SIZE_TINY = '._SL75_'
IMAGE_SIZE_VERY_SMALL = '_SL30_'



def get_image_url(asin, size):
	"""Create an image link to amazon based on the ASIN/ISBN."""
	if not asin:
		# TODO: nosense branch?
		if size == IMAGE_SIZE_SMALL:
			return '/media/img/no_image_small.jpg'
		elif size == IMAGE_SIZE_MEDIUM:
			return '/media/img/no_image_medium.jpg'

	# Strip dashes. Amazon doesn't like ISBNs with dashes.
	asin = asin.replace('-', '')
	return 'http://images.amazon.com/images/P/%s.01%s.jpg' % (asin, size)


def get_product_url(asin):
	return 'http://www.amazon.com/exec/obidos/ASIN/' + asin


def download_cover(release, img_filename="cover.jpg"):
	asin = release.getAsin()
	if not asin:
		return

	img_url = get_image_url(asin, IMAGE_SIZE_LARGE)
	# FIXME: Erm... error handling? urllib.urlretrieve() doesn't seem to have a
	# sensible return value or exceptions...
	urllib.urlretrieve(img_url, img_filename)


# EOF
