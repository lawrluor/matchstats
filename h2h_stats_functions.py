# Head to Head Stats Functions between two Users. Because of the nature of the Set filtering for two Users, the normal User methods for getting Sets cannot be used.
# Optimized to only query the database once for Sets, and once for Matches. Once you call h2h_get_sets_played and h2h_get_matches_played, store in a variable all_sets and all_matches, a list of Set objects representing all the sets the two Users have played toether. From there, use list comprehensions to filter rather than query the database.
# Set and Match lists specifically defined to lessen ambiguity about whih methods to call first to generate Set and Match list.

# given two User tags, returns a list of Set objects representing all the sets they have played together
# call len() on the result of this method to get total number of sets played together

from app import *
from app.models import *
import collections

def h2h_get_mutual_tournaments(tag1, tag2):
  user1_placements = get_tournament_name_and_placing(tag1)
  user2_placements = get_tournament_name_and_placing(tag2)
 
  # if identical keys for tournament (both attended same tournament), return dictionary with keys tournament_name and tuple value containing their respective placement 
  mutual_tournaments = collections.OrderedDict()
  for tournament in user1_placements:
    if tournament in user2_placements:
      mutual_tournaments[tournament] =  user1_placements[tournament], user2_placements[tournament] 
  print mutual_tournaments
  return mutual_tournaments
      
# given user tag, returns a simple dictionary with keys tournament_name and value placement for a tournament a User has attended
def get_tournament_name_and_placing(user_tag):
  user = User.query.filter(User.tag==user_tag).first()
  user_placements = {}

  for tournament_placement in user.tournament_assocs:
    tournament_name = tournament_placement.tournament.name
    placement  = convert_placement(tournament_placement.placement)
    user_placements[tournament_name] = placement

  print user_placements
  return user_placements


# get Sets won by both players, then add them together and sort by id
def h2h_get_sets_played(tag1, tag2):
	user1_won_sets = h2h_get_sets_won(tag1, tag2)
	user2_won_sets = h2h_get_sets_won(tag2, tag1)
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

# In current version of Smashstats, no Match info available
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

# Returns all matches a User played with each Character
# Store this list of Match objects in a variable for later use, like char_matches
# to get number of matches played with specific Character, call len() on this function
def h2h_get_character_played(tag, h2h_matches_played):
	char_matches = {}
	for match in h2h_matches_played:
		if match.winner_char != None and match.winner==tag:
			character = char_matches.setdefault(match.winner_char, [])
			character.append(match)
		if match.loser_char != None and match.loser==tag:
			character = char_matches.setdefault(match.loser_char, [])
			character.append(match)

	return char_matches

# Iterates through char_matches, list of all Matches a User played with a Character, and returns only the matches in which that User won
# To get number of matches won with specific Character, call len() on this function
def h2h_character_wins(winner_tag, char_matches):
	char_won = []
	for match in char_matches:
		if match.winner==winner_tag:
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


