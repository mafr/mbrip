import collections
import mutagen.id3 as id3

from mbrip.utils import errQuit


# TODO: This is just ugly.
class Id3Tag(collections.Mapping):
	"""A read-only view on an ID3 tag.

	Acts like a dict so we can feed it to a Formatter. A future version
	of Mutagen's EasyID3 could replace this.
	"""
	valid_keys = {
		'artist': 'TPE1',
		'title': 'TIT2',
		'album': 'TALB',
		'track': 'TRCK',
		'date': 'TDAT',
	}

	def __init__(self):
		self.frames = { }

	def load(self, filename):
		f = id3.ID3(filename)
		for k, frame_id in Id3Tag.valid_keys.items():
			self.frames[k] = self._get(f, frame_id)

	def __getitem__(self, key):
		return self.frames[key]

	def __iter__(self):
		return iter(self.frames)

	def __len__(self):
		return len(self.frames)

	def _get(self, id3, key):
		if key in id3:
			value = id3[key][0]
			if key == 'TRCK':
				num = value.split('/')[0]
				return u'%02d' % int(num)
			else:
				return value
		else:
			return None

	def __str__(self):
		pass


# TODO: proper testing required!
if __name__ == '__main__':
	f = Id3Tag()
	f.load('03_-_Kind_Generous.mp3')

	print repr(f['title'])
	print repr(f['track'])

# EOF
