import sys
sys.path.insert(0,'..')
sys.path.insert(0,'../sanitize')

from app.models import *
import urllib3
import json
import requests
import challonge
from pprint import pprint

from date_utils import *
from trueskill_functions import *

class TournamentInfo:
	'''
	Object to carry tournament information across functions
	'''
	id = 0
	parent=""
	official_title=""
	host=""
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
		url=%s, entrants=%s, bracket_type=%s, game_type=%s)' % (self.id, self.parent, self.name,
		self.region, self.date, self.official_title, self.host, 
		self.url, self.entrants, self.bracket_type, self.game_type)


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

# Master function, analagous to parse_bracket_info in parse_smashgg_info.py
# Only challonge_id for tournament strictly necessary, this parameter will be found and fed by another func.
def process_tournament(challonge_id, tournament_name, tournament_region, tournament_date):
	tournament = challonge.tournaments.show(challonge_id)
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
		process_bracket_info(bracket_json, tournament_info)

	return "FINISHED"

# Parses a bracket for entrant and set information
def process_bracket_info(bracket, tournament_info):
	# Generate sub_bracket name using parent tournament name and sub_bracket name
	bracket_name = tournament_info.name + ' | ' + bracket['name']

	# With created sub_bracket name and parent tournament info, create new TournamentInfo object
	bracket_info = TournamentInfo(bracket_name, tournament_info.region, tournament_info.date)
	
	bracket_info.id = bracket['id']
	bracket_info.url = bracket['full-challonge-url']
	bracket_info.entrants = bracket['participants-count']
	bracket_info.official_title = bracket['name']
	bracket_info.host = bracket['subdomain']

	# Inherited from parent tournament
	bracket_info.parent = tournament_info.name
	bracket_info.bracket_type = tournament_info.bracket_type
	bracket_info.game_type = tournament_info.game_type

	print bracket_info

	sub_tournament = import_sub_tournament_info(bracket_info)
	# Process bracket entrants and sets, passing bracket object info
	process_entrants(bracket_info, sub_tournament)


def process_entrants(bracket_info, sub_tournament):
	entrants = challonge.participants.index(bracket_info.id)

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
		print entrant
		print '\n'

	if entrant_list[0].sub_placing is None or entrant_list[0].super_placing is None:
		# gotta parse
		print True

	import_entrants(entrant_list, sub_tournament)

# Import entrants and create User objects in database, given SubTournament object and entrant list
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

# Build tournament_info object by assigning values to it from queried tournament JSON
def process_tournament_info(tournament_info, tournament):
	pprint(tournament)
	
	tournament_info.id = tournament['id']
	tournament_info.official_title = tournament['name']
	tournament_info.host = tournament['subdomain']
	tournament_info.bracket_type = tournament['tournament-type']
	tournament_info.entrants = tournament['participants-count']
	if tournament['game-name'] is not None:
		tournament_info.game_type = tournament['game-name']
	else:
		tournament_info.game_type = "Super Smash Bros. Melee"

	if tournament['started-at'] is not None:
		tournament_info.date = tournament['started-at']
	else:
		tournament_info.date = convert_date(tournament_info.date)
	tournament_info.url = tournament['full-challonge-url']

	print tournament_info
	return tournament_info

# Given processed tournament_info object from process_tournament_info, add Tournament object to database with the appropriate information
# Returns Tournament object (the parent/master tournament)
def import_tournament_info(tournament_info):
	new_tournament = Tournament(official_title=tournament_info.official_title,
								host=tournament_info.host,
								url=tournament_info.url,
								entrants=tournament_info.entrants,
								bracket_type=tournament_info.bracket_type,
								game_type=tournament_info.game_type,
								date=tournament_info.date,
								name=tournament_info.name
								)

	db.session.add(new_tournament)
	db.session.commit()

	# add tournament_region; if None, then it adds None
	found_region = Region.query.filter(Region.region==tournament_info.region).first()
	if found_region is not None:
		found_region.adopt_tournament(new_tournament.name)

	db.session.commit()
	return new_tournament

# Given processed tournament_info object from process_tournament_info, add Tournament object to database with the appropriate information
# Returns Tournament object (the parent/master tournament)
def import_sub_tournament_info(sub_tournament_info):
	new_sub_tournament = SubTournament(official_title=sub_tournament_info.official_title,
								url=sub_tournament_info.url,
								entrants=sub_tournament_info.entrants,
								bracket_type=sub_tournament_info.bracket_type,
								date=sub_tournament_info.date,
								name=sub_tournament_info.name
								)

	db.session.add(new_sub_tournament)

	# add tournament_region; if None, then it adds None
	new_sub_tournament.region = Region.query.filter(Region.region==sub_tournament_info.region).first()
	
	# associate with parent Tournament
	parent_tournament = Tournament.query.filter(Tournament.name==sub_tournament_info.parent).first()
	parent_tournament.sub_tournaments.append(new_sub_tournament)

	db.session.commit()
	return new_sub_tournament

