import re

def queryUser(prompt, default, validator=lambda x: True):
	try:
		while True:
			value = raw_input(prompt).strip()
			if value == '':
				return default

			if validator(value):
				return value
			else:
				print "Invalid choice."
	except EOFError:
		print
		return default


def parseSpan(span):
	spanRE = re.compile('^\s*(\d+)\s*(?:-\s*(\d+)\s*)?$')
	elem = { }

	for word in re.split(',', span):
		m = spanRE.match(word)

		if not m:
			raise SyntaxError

		start = int( m.group(1) )

		if m.group(2):
			stop = int( m.group(2) )
		else:
			stop = start

		for i in range(start, stop+1):
			elem[i] = 1

	return sorted(elem.keys(), lambda a, b: cmp(a, b))


class Menu:
	def __init__(self, default, title):
		self.default = default
		self.title = title
		self.choices = [ ]

	def addChoice(self, selector, description):
		self.choices.append((selector, description))

	def showMenu(self):
		print
		if self.title:
			print self.title
			print
		for (sel, descr) in self.choices:
			if sel is None:
				print
			else:
				print " (%s) %s" % (sel, descr)
		print

		validChoices = [x[0] for x in self.choices]
		isValid = lambda x: x in validChoices
		prompt = 'select (default: %s) > ' % self.default
		return queryUser(prompt, self.default, isValid)

# EOF
