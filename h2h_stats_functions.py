# Head to Head Stats Functions between two Users. Because of the nature of the Set filtering for two Users, the normal User methods for getting Sets cannot be used.
# Optimized to only query the database once for Sets, and once for Matches. Once you call h2h_get_sets_played and h2h_get_matches_played, store in a variable all_sets and all_matches, a list of Set objects representing all the sets the two Users have played toether. From there, use list comprehensions to filter rather than query the database.
# Set and Match lists specifically defined to lessen ambiguity about whih methods to call first to generate Set and Match list.

# given two User tags, returns a list of Set objects representing all the sets they have played together
# call len() on the result of this method to get total number of sets played together

from app import *
from app.models import *

def h2h_get_sets_played(tag1, tag2):
	user1_won_sets = Set.query.filter(and_(Set.winner_tag==tag1, Set.loser_tag==tag2)).all()
	user2_won_sets = Set.query.filter(and_(Set.winner_tag==tag2, Set.loser_tag==tag1)).all()
  # Any set user2 has won, user1 has lost, so user2_won == number of sets user1 has lost.

	h2h_all_sets = user1_won_sets + user2_won_sets
	h2h_all_sets = sorted(h2h_all_sets, key=lambda x: x.id)
	return h2h_all_sets


# given two User tags, returns a list of Set objects representing Sets between the two Users in which the first User has won.
# call len() on the result of this method to get number of sets winner has won vs the loser
def h2h_get_sets_won(winner, loser, h2h_all_sets):
	sets_won = []
	for set in h2h_all_sets:
		if set.winner_tag == winner:
			sets_won.append(set)

	return sets_won


# given two User tags, returns a list of Match objects representing the total number of matches they have played together.
def h2h_get_matches_played(tag1, tag2, h2h_all_sets):
	h2h_all_matches = []
	for set in h2h_all_sets:
		h2h_all_matches += set.matches.all()

	return h2h_all_matches
		

# given two User tags, returns a list of Match objects representing Matches between the two Users in which the first User has won.
def h2h_get_matches_won(winner, loser, h2h_all_matches):
	won_matches = []
	for match in h2h_all_matches:
		if match.winner == winner:
			won_matches.append(match)

	return won_matches