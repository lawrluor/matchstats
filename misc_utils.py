# Exception for UnicodeError during printing, if unicode character cannot be converted, skip the print
def print_ignore(input):
	try:
		print input
	except UnicodeError:
		pass

# Use regex expression for this?
# Sanitizes argument from url_for that has URL escape characters in it
def sanitize_url(tournament_name):
	tournament_name = tournament_name.replace("%20", ' ')
	tournament_name = tournament_name.replace("%2F", '/')
	tournament_name = tournament_name.replace("%2D", '-')
	tournament_name = tournament_name.replace("%2E", '.')
	return tournament_name