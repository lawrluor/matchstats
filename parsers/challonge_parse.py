import sys
sys.path.insert(0,'..')
sys.path.insert(0,'../sanitize')

from app.models import *
import urllib3
from bs4 import BeautifulSoup
import json
import requests
import challonge
from pprint import pprint

from date_utils import *
from trueskill_functions import *
from misc_utils import print_ignore

class TournamentInfo:
	'''
	Object to carry tournament information across functions
	'''
	id = 0
	parent=""
	official_title=""
	host=""
	public_url=""
	url=""
	entrants=""
	bracket_type=""
	game_type=""

	def __init__(self, tournament_name, tournament_region, tournament_date):
		self.name = tournament_name
		self.region = tournament_region
		self.date = tournament_date

	def __str__(self):
		return 'TournamentInfo(id=%s, parent=%s, name=%s, region=%s, date=%s, official_title=%s, host=%s,\
		url=%s, public_url=%s, entrants=%s, bracket_type=%s, game_type=%s)' % (self.id, self.parent, self.name, self.region, 
		self.date, self.official_title, self.host, self.public_url, self.url, self.entrants, self.bracket_type, self.game_type)


class EntrantInfo:
	'''
	Object to carry Entrant info
	'''
	id = 0
	player_tag = ""
	account_name = ""
	sub_seed = 0
	super_seed = 0
	sub_placing = 0
	super_placing = 0

	def __init__(self, player_tag):
		self.player_tag = player_tag

	def __str__(self):
		return 'EntrantInfo(id=%s, tag=%s, account_name=%s, sub_seed=%s, super_seed=%s, sub_placing=%s, super_placing=%s)' % \
		(self.id, self.player_tag, self.account_name, self.sub_seed, self.super_seed, self.sub_placing, self.super_placing)

class SetInfo:
	'''
	Object to carry Set info
	'''
	id = 0
	round_number = 0
	round_name = ""
	winner_id = 0
	loser_id = 0
	winner_tag = ""
	loser_tag = ""
	winner_score = 0
	loser_score = 0
	total_matches = winner_score+loser_score

	def __init__(self, id):
		self.id = id

	def __str__(self):
		return 'SetInfo(id=%s, round_number=%s, round_name=%s, winner_id=%s, loser_id=%s, winner_tag=%s, loser_tag=%s, winner_score=%s, loser_score=%s, total_matches=%s)' % \
		(self.id, self.round_number, self.round_name, self.winner_id, self.loser_id, self.winner_tag, self.loser_tag, self.winner_score, self.loser_score, self.total_matches)

# Helper function to parse Challonge scores from set['scores-csv'] in the form 'x-y'
# Returns tuple of winner_score, loser_score
def parse_scores(scores):
	if scores is None:
		return -1, -1

	# Separate winner and loser scores
	score_list = scores.split('-')
	# print score_list[0], type(score_list[0]), len(score_list[0])
	# print score_list[1], type(score_list[1]), len(score_list[1])
	# print '\n'

	# Catch invalid scores
	if len(score_list[0])<1 or len(score_list[1])<1:
		return -1, -1
	# In case of Bracket Reset in Grand Finals, scores is 3-char string like so: 0,1
	# Actually, I'm not sure when this happens. If so, treat like a glitch
	# First example: process_tournament("http://challonge.com/happyblackhistorymonth", "UCONN", "New England", "February 29, 2016")
	# Loser's Finals match not recorded properly. S2B over Scyzel 3-0, recorded as 1-0. 
	# Extra Blue text indicating "Best of X" Match on this Challonge page
	elif len(score_list[0])>1 or len(score_list[1])>1:
		print "---THIS IS A BUG---"
		if len(score_list[0])>1:
			score0 = int(score_list[0][0].strip())
			score1 = int(score_list[1].strip())
		elif len(score_list[1])>1:
			score0 = int(score_list[0].strip())
			score1 = int(score_list[1][0].strip())
	else:
		score0 = int(score_list[0])
		score1 = int(score_list[1])
		
	winner_score = max(score0, score1)
	loser_score = min(score0, score1)
	return winner_score, loser_score

# Parse challonge url in form "http://bigbluees.challonge.com/NGP46"
# or "http://challonge.com/fi2f9gcu" (without subdomain)
# return plain tournament_string, or subdomain-tournament_string if subdomain exists
def parse_url(challonge_url):
	challonge_index = challonge_url.rindex("challonge.com")
	http_index = challonge_url.rindex("http://")
	subdomain = challonge_url[http_index+7:challonge_index-1]
	tournament_string = challonge_url[challonge_index+14:]

	if len(subdomain)==0:
		return tournament_string
	else:
		return subdomain+ '-' + tournament_string

# Given tournament_url, grab standings page. Necessary when tournament not finished, and participant['final_rank'] is None
# RIGHT NOW BLOCKED
def parse_standings(tournament_url):
	conn = urllib3.connection_from_url(tournament_url)
	r = conn.request("GET", tournament_url)
	soup = BeautifulSoup(r.data)
	print soup.prettify()

# Alternative to parsing standings page, calculate and assign placements after each set played
def calculate_standings(set_list):
	round_numbers = [set.round_number for set in set_list]
	last_loser_round = min(round_numbers) * -1
	last_winner_round = max(round_numbers)
	
	placings = {"last_winner_round" : last_winner_round,
				last_loser_round : 3}
	counter = 1
	current_round = last_loser_round
	increment = 1
	for i in range(1, last_loser_round):
		current_round = (last_loser_round - i)
		if counter < 2:
			placings[current_round] = placings[current_round + 1] + increment
			counter += 1
		else:
			placings[current_round] = placings[current_round + 1] + increment
			increment = increment * 2
			counter = 1
	print "---PLACINGS---", placings
	return placings

# Build tournament_info object by assigning values to it from queried tournament JSON
def process_tournament_info(tournament_info, tournament):
	# pprint(tournament)
	
	tournament_info.id = tournament['id']
	tournament_info.official_title = tournament['name']
	tournament_info.host = tournament['subdomain']
	tournament_info.entrants = tournament['participants-count']
	if tournament['game-name'] is None or tournament['game-name']=='':
		tournament_info.game_type = "Super Smash Bros. Melee"
	else:
		tournament_info.game_type = tournament['game-name']

	if tournament['started-at'] is not None:
		tournament_info.date = tournament['started-at']
	else:
		tournament_info.date = convert_int_date(tournament_info.date)
	tournament_info.url = tournament['full-challonge-url']
	return tournament_info

# Parses a sub_bracket for entrant and set information
def process_bracket_info(sub_bracket, tournament_info, final_bracket):
	# Generate sub_bracket name using parent tournament name and sub_bracket name
	if final_bracket==True:
		bracket_name = tournament_info.name
	else:
		bracket_name = tournament_info.name + ' | ' + sub_bracket['name']

	# With created sub_bracket name and parent tournament info, create new TournamentInfo object
	sub_bracket_info = TournamentInfo(bracket_name, tournament_info.region, tournament_info.date)
	sub_bracket_info.id = sub_bracket['id']
	sub_bracket_info.url = sub_bracket['full-challonge-url']
	sub_bracket_info.entrants = sub_bracket['participants-count']
	sub_bracket_info.official_title = sub_bracket['name']
	sub_bracket_info.host = sub_bracket['subdomain']

	# Inherited from parent tournament header
	sub_bracket_info.parent = tournament_info.name
	sub_bracket_info.bracket_type = tournament_info.bracket_type
	sub_bracket_info.game_type = tournament_info.game_type
	print sub_bracket_info

	sub_tournament = import_sub_tournament_info(sub_bracket_info)
	# Process bracket entrants and sets, passing bracket object info
	entrant_list = process_entrants(sub_bracket_info, sub_tournament)
	process_sets(sub_bracket_info, entrant_list, sub_tournament)

def process_entrants(sub_bracket_info, sub_tournament):
	entrants = challonge.participants.index(sub_bracket_info.id)
	# pprint(entrants)

	entrant_list = []
	for entrant in entrants:
		entrant_info = EntrantInfo(entrant['display-name'])
		entrant_info.id = int(entrant['id'])
		entrant_info.account_name = entrant['name']
		entrant_info.sub_seed = entrant['seed']
		entrant_info.super_seed = entrant['seed']
		entrant_info.sub_placing = entrant['final-rank'] # If tournament not finished, None. have to parse
		entrant_info.super_placing = entrant['final-rank'] # If tournament not finished, None. have to parse
		entrant_list.append(entrant_info)

	print "\n---ENTRANTS---"
	for entrant in entrant_list:
		print_ignore(entrant)

	import_entrants(entrant_list, sub_tournament)
	return entrant_list

def process_sets(sub_bracket_info, entrant_list, sub_tournament):
	sets = challonge.matches.index(sub_bracket_info.id)
	# pprint(sets)

	set_list = []
	for set in sets:
		set_info = SetInfo(set['id'])
		winner_score, loser_score = parse_scores(set['scores-csv'])
		if winner_score<0 or loser_score<0:
			continue
		else:
			set_info.winner_score = winner_score
			set_info.loser_score = loser_score
			set_info.total_matches = winner_score + loser_score

		set_info.round_number = set['round']
		set_info.round_name = set['identifier']
		set_info.winner_id = set['winner-id']
		set_info.loser_id = set['loser-id']

		try:
			winner = next(entrant for entrant in entrant_list if entrant.id==set['winner-id'])
			loser = next(entrant for entrant in entrant_list if entrant.id==set['loser-id'])
		except StopIteration:
			print "StopIteration Error detected. Tournament:", sub_tournament.name
			# Later: write code to exit, and delete Tournament
			continue

		set_info.winner_tag = winner.player_tag
		set_info.loser_tag = loser.player_tag

		set_list.append(set_info)

	if winner.sub_placing is None and loser.sub_placing is None:
		assign_placings = True
	else:
		assign_placings = False

	import_sets(set_list, sub_tournament, assign_placings)


# Given processed tournament_info object from process_tournament_info, add Tournament object to database with the appropriate information
# Returns Tournament object (the parent/master tournament)
def import_tournament_info(tournament_info):
	new_tournament_header = TournamentHeader(official_title=tournament_info.official_title,
								host=tournament_info.host,
								url=tournament_info.url,
								public_url=tournament_info.url,
								entrants=tournament_info.entrants,
								game_type=tournament_info.game_type,
								date=tournament_info.date,
								name=tournament_info.name
								)
	db.session.add(new_tournament_header)
	db.session.commit()

	# add tournament_region; if None, then it adds None
	found_region = Region.query.filter(Region.region==tournament_info.region).first()
	new_tournament_header.region = found_region

	db.session.commit()
	print "---TOURNAMENT HEADER---", new_tournament_header
	return new_tournament_header

# Given processed tournament_info object from process_tournament_info, add Tournament object to database with the appropriate information
# Returns Tournament object (the parent/master tournament)
def import_sub_tournament_info(sub_tournament_info):
	new_sub_tournament = Tournament(official_title=sub_tournament_info.official_title,
								url=sub_tournament_info.url,
								public_url=sub_tournament_info.url,
								entrants=sub_tournament_info.entrants,
								bracket_type=sub_tournament_info.bracket_type,
								date=sub_tournament_info.date,
								name=sub_tournament_info.name
								)
	db.session.add(new_sub_tournament)

	# associate with TournamentHeader
	tournament_header = TournamentHeader.query.filter(TournamentHeader.name==sub_tournament_info.parent).first()
	tournament_header.sub_tournaments.append(new_sub_tournament)
	new_sub_tournament.region = new_sub_tournament.header.region

	db.session.commit()
	print "---SUBTOURNAMENT---", new_sub_tournament
	return new_sub_tournament

# Import entrants and create User objects in database, given (sub) Tournament object and entrant list
def import_entrants(entrant_list, sub_tournament):
	for entrant in entrant_list:
		player_tag = entrant.player_tag
		checked_player = check_set_user(player_tag, sub_tournament.region)

		sub_tournament.placements.append(Placement(
										tournament_id=sub_tournament.id,
										tournament_name=sub_tournament.name,
										user_id=checked_player.id,
										placement=entrant.sub_placing
										))
	sub_tournament.entrants = len(entrant_list)
	db.session.commit()
	return sub_tournament

# Import sets, create Set objects in database and associate them with Tournament
def import_sets(set_list, sub_tournament, assign_placings):
	if assign_placings is True:
		placings_dict = calculate_standings(set_list)

	print "---SETS---"
	for set in set_list:
		# After calling check_set_user, Users by tag will exist in database in any case.
		# stores User object in respective variables
		winner_tag = set.winner_tag.strip()
		winner_user = check_set_user(winner_tag, sub_tournament.region)
		loser_tag = set.loser_tag.strip()
		loser_user = check_set_user(loser_tag, sub_tournament.region)

		# Query for associated Tournament
		if sub_tournament.name is not None:
			assocs_tournament = Tournament.query.filter(Tournament.name==sub_tournament.name).first()
		else:
			print "Tournament not Found"

		if assign_placings is True:
			if (-1 * set.round_number) in placings_dict:
				print "Loser places", placings_dict[(-1 * set.round_number)]
				found_placement = Placement.query.filter(and_(Placement.tournament_name==assocs_tournament.name, Placement.user_id==loser_user.id)).first()
				found_placement.placement = placings_dict[(-1 * set.round_number)]
			elif set.round_number==placings_dict["last_winner_round"]:
				winner_placement = Placement.query.filter(and_(Placement.tournament_name==assocs_tournament.name, Placement.user_id==winner_user.id)).first()
				loser_placement = Placement.query.filter(and_(Placement.tournament_name==assocs_tournament.name, Placement.user_id==loser_user.id)).first()
				winner_placement.placement = 1
				loser_placement.placement = 2

		new_set = Set(tournament_id=assocs_tournament.id,
	                  tournament_name=assocs_tournament.name,
	                  round_type=set.round_number,
	                  winner_tag=winner_user.tag,
	                  loser_tag=loser_user.tag,
	                  winner_id=winner_user.id,
	                  loser_id=loser_user.id,
	                  winner_score=set.winner_score,
	                  loser_score=set.loser_score,
	                  total_matches=set.total_matches)
		db.session.add(new_set) 
		print_ignore(set)

		# update User trueskill ratings based on Set winner and loser
		update_rating(winner_user, loser_user)

	db.session.commit()

# MASTER function, analagous to parse_bracket_info in parse_smashgg_info.py
# Only url for tournament strictly necessary, this parameter will be found and fed by another func.
def process_tournament(tournament_url, tournament_name, tournament_region, tournament_date):
	print "\nPROCESSING:", tournament_name
	tournament = challonge.tournaments.show(parse_url(tournament_url))
	tournament_info = TournamentInfo(tournament_name, tournament_region, tournament_date)

	# Get general info about Tournament and return+update tournament_info object, then import it into database
	tournament_info = process_tournament_info(tournament_info, tournament)
	import_tournament_info(tournament_info)

	# Find all sub brackets - NOT DONE YET
	# Also need function to manually parse pool brackets not originally associated with master tournament

	# brackets = SHOW sub brackets
	bracket_list = []
	# for x in brackets:
	#	bracket_json = challonge.tournaments.show(bracket)
	#	bracket_list.append(bracket_json)
	#	process_bracket_info(bracket_json, tournament_info)
	
	bracket_list.append(tournament)
	# for each sub bracket, pass the sub bracket JSON tournament object, and the associated parent tournament_info
	for bracket_json in bracket_list:
		if len(bracket_list)==1:
			final_bracket = True
		else:
			final_bracket = False
		process_bracket_info(bracket_json, tournament_info, final_bracket)

	print "FINISHED"
	final_tournament = TournamentHeader.query.filter(TournamentHeader.name==tournament_name).first()
	return final_tournament
