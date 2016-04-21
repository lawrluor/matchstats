# Exception for UnicodeError during printing, if unicode character cannot be converted, skip the print
def print_ignore(input):
	try:
		print input
	except UnicodeError:
		pass