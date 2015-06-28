# Head to Head Stats Functions between two Users. Because of the nature of the Set filtering for two Users, the normal User methods for getting Sets cannot be used.
# Optimized to only query the database once for Sets, and once for Matches. Once you call h2h_get_sets_played and h2h_get_matches_played, store in a variable all_sets and all_matches, a list of Set objects representing all the sets the two Users have played toether. From there, use list comprehensions to filter rather than query the database.
# Set and Match lists specifically defined to lessen ambiguity about whih methods to call first to generate Set and Match list.

# given two User tags, returns a list of Set objects representing all the sets they have played together
# call len() on the result of this method to get total number of sets played together

from app import *
from app.models import *

# Initialize dictionary with no initial values, only Stages as keys


def h2h_get_sets_played(tag1, tag2):
	user1_won_sets = Set.query.filter(and_(Set.winner_tag==tag1, Set.loser_tag==tag2)).all()
	user2_won_sets = Set.query.filter(and_(Set.winner_tag==tag2, Set.loser_tag==tag1)).all()
  # Any set user2 has won, user1 has lost, so user2_won == number of sets user1 has lost.

	h2h_sets_played = user1_won_sets + user2_won_sets
	h2h_sets_played = sorted(h2h_sets_played, key=lambda x: x.id)
	return h2h_sets_played


# given two User tags, returns a list of Set objects representing Sets between the two Users in which the first User has won.
# call len() on the result of this method to get number of sets winner has won vs the loser
def h2h_get_sets_won(winner_tag, loser_tag):
	sets_won = Set.query.filter(and_(Set.winner_tag==winner_tag, Set.loser_tag==loser_tag)).all()
	return sets_won


# given two User tags, returns a list of Match objects comprised of all matches they have played together.
def h2h_get_matches_played(h2h_sets_played):
	h2h_matches_played = []
	for set in h2h_sets_played:
		h2h_matches_played += set.matches

	return h2h_matches_played


#	user1_won_matches = h2h_get_matches_won(tag1, tag2)
#	user2_won_matches = h2h_get_matches_won(tag2, tag1)
#	h2h_matches_played = user1_won_matches + user2_won_matches
#	return h2h_matches_played


# given two User tags, returns a list of Match objects representing Matches between the two Users in which the first User has won.
def h2h_get_matches_won(winner_tag, loser_tag, h2h_matches_played):
	won_matches = []
	for match in h2h_matches_played:
		if match.winner == winner_tag:
			won_matches.append(match)

	return won_matches


#	return Match.query.filter(and_(Match.winner==winner, Match.loser==loser).all()


# Populates dictionary with stage names for keys with a list of Match objects for each Match played on that stage.
# Store this dictionary in a variable for later use, like h2h_stages_played
# Access information by calling len(h2h_stages_played[key]) to find total number of matches played on that stage
def h2h_get_stages_played(h2h_matches_played):
	Stages = {'Battlefield' : [], 
						'Dream Land' : [], 
						'Final Destination' : [], 
						'Fountain of Dreams' : [],
						'Pokemon Stadium' : [], 
						'Yoshi\'s Story' : [],
						'Other': []}
	for match in h2h_matches_played:
		for key in Stages:
			if match.stage == key:
				Stages[key].append(match)

	return Stages

# given the Stages dictionary and a User tag, get the win count for that User on each Stage.
# Store this dictionary in a variable for later use, like winnertag_stages_won
# Access that information by calling winnertag_stages_won[key] to find total number of matches won on that stage
def h2h_get_stages_won(winner_tag, Stages):
	stage_win_count = {'Battlefield' : 0, 
						'Dream Land' : 0, 
						'Final Destination' : 0, 
						'Fountain of Dreams' : 0,
						'Pokemon Stadium' : 0, 
						'Yoshi\'s Story' : 0,
						'Other' : 0}
	for key in Stages:
		for i in range(len(Stages[key])):
			if Stages[key][i].winner == winner_tag:
				stage_win_count[key] += 1

	return stage_win_count

# Returns all matches a User played with a Character
# Store this list of Match objects in a variable for later use, like char_matches
# to get number of matches played with specific Character, call len() on this function
def h2h_get_character_played(tag, character, h2h_matches_played):
	char_matches = []
	for match in h2h_matches_played:
		if (match.winner==tag and match.winner_char==character) or (match.loser==tag and match.loser_char==character):
			char_matches.append(match)

	return char_matches

# Iterates through char_matches, list of all Matches a User played with a Character, and returns only the matches in which that User won
# To get number of matches won with specific Character, call len() on this function
def h2h_character_wins(winner_tag, char_matches):
	char_won = []
	for match in char_matches:
		if match.winner==winner_tag:
			char_won.append(match)

	return char_won

