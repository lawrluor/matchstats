from app import *
from app.models import *
import collections
from operator import attrgetter
from sort_utils import sort_placementlist, sort_setlist

"""
Head to Head Stats Functions between two Users.

Sets and Users are NOT associated through ORM and are instead associated by
joins. We have provided utility functions to aid in this association.

Set and Match lists specifically defined to lessen ambiguity about which methods
to call first to generate Set and Match list.
"""

class UserPlacements:
  '''
  To store information about User's placements at tournaments in function 'user'
  Identical to UserPlacements object in views.py
  '''
  tournament = ""
  placement = 0
  seed = 0

  def __init__(self, tournament_name):
    self.tournament_name = tournament_name

  def __str__(self):
    return 'UserPlacements(tournament_name=%s, placement=%s, seed=%s, tournament=%s)' % \
    (self.tournament_name, self.placement, self.seed, self.tournament)


def h2h_get_mutual_tournaments(user1, user2):
  '''
  given two User objects, returns list of lists containing two UserPlacements objects (which contain tournament_name,
  placement, and seed), corresponding to user1 and user2 for each mutual tournament attended

  call len() on the result of this method to get total number of tournaments
  attended together.
  '''

  # Debug this
  user1_placements = get_placement_info(user1)
  user2_placements = get_placement_info(user2)
 
  # if identical names for tournament (both attended same tournament), add to list of mutual tournaments
  mutual_tournaments = []
  for user1_placement in user1_placements:
    mutual_tournament = next((user2_placement for user2_placement in user2_placements if user1_placement.tournament_name==user2_placement.tournament_name), None)
    if mutual_tournament is not None:
      mutual_tournaments.append([user1_placement, mutual_tournament])
  return mutual_tournaments

# Make this a class function in models?
def get_placement_info(user):
  '''
  Returns list of UserPlacements object, each storing info for each tournament, placement, and seed
  '''
  user_placements_sorted = sort_placementlist(user.tournament_assocs)
  
  placings = []
  for tournament_placement in user_placements_sorted:
    user_placement = UserPlacements(tournament_placement.tournament.name)
    user_placement.tournament = tournament_placement.tournament
    user_placement.placement = convert_placement(tournament_placement.placement)
    placings.append(user_placement)
  return placings


def h2h_get_sets_played(user1, user2):
  """Given two users, returns all sets played between them, sorted by set id.

  Args:
      user1 : User(models.py) : First user object to query for sets.
      user2 : User(models.py) : Second user object to query for sets.

  Returns:
      A list of Set(models.py) objects sorted by set id of sets played between
      the two users.
  """
  user1_won_sets = h2h_get_sets_won(user1, user2)
  user2_won_sets = h2h_get_sets_won(user2, user1)
  # Any set user2 has won, user1 has lost, so user2_won == number of sets user1 has lost.

  h2h_sets_played = user1_won_sets + user2_won_sets
  h2h_sets_played = sort_setlist(h2h_sets_played)
  return h2h_sets_played


# given two User objects, returns a list of Set objects representing Sets between the two Users in which the first User has won.
# call len() on the result of this method to get number of sets winner has won vs the loser
def h2h_get_sets_won(winner, loser):
	sets_won = Set.query.filter(and_(Set.winner_tag==winner.tag, Set.loser_tag==loser.tag)).all()
	return sets_won


# given two User tags, returns a list of Match objects comprised of all matches they have played together.
def h2h_get_matches_played(h2h_sets_played):
	h2h_matches_played = []
	for set in h2h_sets_played:
		h2h_matches_played += set.matches

	return h2h_matches_played

# In current version of Smashstats, no Match info available
#	user1_won_matches = h2h_get_matches_won(tag1, tag2)
#	user2_won_matches = h2h_get_matches_won(tag2, tag1)
#	h2h_matches_played = user1_won_matches + user2_won_matches
#	return h2h_matches_played


# given two User tags, returns a list of Match objects representing Matches between the two Users in which the first User has won.
def h2h_get_matches_won(winner, loser, h2h_matches_played):
	won_matches = []
	for match in h2h_matches_played:
		if match.winner == winner.tag:
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
def h2h_get_stages_won(winner, Stages):
	stage_win_count = {'Battlefield' : 0, 
						'Dream Land' : 0, 
						'Final Destination' : 0, 
						'Fountain of Dreams' : 0,
						'Pokemon Stadium' : 0, 
						'Yoshi\'s Story' : 0,
						'Other' : 0}
	for key in Stages:
		for i in range(len(Stages[key])):
			if Stages[key][i].winner == winner.tag:
				stage_win_count[key] += 1

	return stage_win_count

# Returns all matches a User played with each Character
# Store this list of Match objects in a variable for later use, like char_matches
# to get number of matches played with specific Character, call len() on this function
def h2h_get_character_played(user, h2h_matches_played):
	char_matches = {}
	for match in h2h_matches_played:
		if match.winner_char != None and match.winner==user.tag:
			character = char_matches.setdefault(match.winner_char, [])
			character.append(match)
		if match.loser_char != None and match.loser==user.tag:
			character = char_matches.setdefault(match.loser_char, [])
			character.append(match)

	return char_matches

# Iterates through char_matches, list of all Matches a User played with a Character, and returns only the matches in which that User won
# To get number of matches won with specific Character, call len() on this function
def h2h_character_wins(winner, char_matches):
	char_won = []
	for match in char_matches:
		if match.winner==winner.tag:
			char_won.append(match)

	return char_won

# helper function to convert placement integers to actual placement strings (i.e. 1 becomes 1st, 2 becomes 2nd)
def convert_placement(integer):
  if integer % 10 == 1:
    if integer != 11:
      placement = str(integer) + "st"
    else:
      placement = "11th"
  elif integer % 10 == 2:
    if integer != 12:
      placement = str(integer) + "nd" 
    else:
      placement = "12th"
  elif integer % 10 == 3:
    if integer != 13:
      placement = str(integer) + "rd"
    else:
      placement = "13th"
  else:
    placement = str(integer) + "th"

  return placement
