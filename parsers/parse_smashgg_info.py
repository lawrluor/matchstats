import sys
sys.path.insert(0,'..')
sys.path.insert(0,'../sanitize')

from app.models import *
import urllib3
import json
import requests
from pprint import pprint

from date_utils import *
from trueskill_functions import *
from misc_utils import print_ignore

# To be converted into TournamentHeader objects
class TournamentInfo:
	'''
	Object to carry tournament information across functions
	'''
	parent=""
	title=""
	host=""
	public_url=""
	url=""
	entrants=0
	game_type=""
	bracket_type=""

	def __init__(self, id, name, region, date):
		self.id = id
		self.name = name
		self.region = region
		self.date = date

	def __str__(self):
		return 'TournamentInfo(id=%s, parent=%s, name=%s, region=%s, date=%s, title=%s, host=%s, \
		public_url=%s, url=%s, entrants=%s, bracket_type=%s, game_type=%s)' % (self.id, self.parent, self.name, self.region, 
		self.date, self.title, self.host, self.public_url, self.url, self.entrants, self.bracket_type, self.game_type)

class SubBracket:
	'''
	Object to carry SubBracket info
	'''
	phase_id = 0
	wave_id = 0
	name = ""
	url = ""

	def __init__(self, id):
		self.id = id

	def __str__(self):
		return 'SubBracket(id=%s, phase_id=%s, wave_id=%s, name=%s, url=%s)' % \
		(self.id, self.phase_id, self.wave_id, self.name, self.url)

class EntrantInfo:
	'''
	Object to carry Entrant info
	'''
	entrant_id = 0
	entrant_name = ""
	player_tag = ""
	player_prefix = ""
	player_id = 0
	player_region = ""
	player_country = ""
	player_state = ""
	player_sub_seed = ""
	player_super_seed = ""
	player_sub_placing = ""
	player_super_placing = ""

	def __init__(self, id, entrant_name):
		# Unique to current tournament
		self.entrant_id = id
		self.entrant_name = entrant_name

	def __str__(self):
		return 'EntrantInfo(entrant_id=%s, entrant_name=%s, player_tag=%s, player_prefix=%s, player_id=%s, player_region=%s, player_country=%s, player_state=%s, player_sub_seed=%s, player_super_seed=%s, player_sub_placing=%s, player_super_placing=%s)' % \
		(self.entrant_id, self.entrant_name, self.player_tag, self.player_prefix, self.player_id, self.player_region, self.player_country, self.player_state, self.player_sub_seed, self.player_super_seed, self.player_sub_placing, self.player_super_placing)

class SetInfo:
	'''
	Object to carry Set info
	'''
	id = 0
	round_number = 0
	round_text = ""
	best_of = 0
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
		return 'SetInfo(id=%s, round_number=%s, round_text=%s, best_of=%s, winner_id=%s, loser_id=%s, winner_tag=%s, loser_tag=%s, winner_score=%s, loser_score=%s, total_matches=%s)' % \
		(self.id, self.round_number, self.round_text, self.best_of, self.winner_id, self.loser_id, self.winner_tag, self.loser_tag, self.winner_score, self.loser_score, self.total_matches)

# Gets the tournament header info and stores it in TournamentInfo object
def parse_tournament_info(tournament_id, tournament_url, tournament_name, tournament_region, tournament_date):
	info_url = "https://api.smash.gg/event/" + tournament_id
	info = requests.get(info_url)
	info_json = info.json()
	# pprint(info_json)

	tournament_info = TournamentInfo(tournament_id, tournament_name, tournament_region, tournament_date)
	if info_json['entities']['event'].get("startedAt") is not None:
		tournament_info.date = convert_int_date(info_json['entities']['event'].get("startedAt"))
	else:
		tournament_info.date = convert_int_date(tournament_date)

	tournament_info.public_url = tournament_url
	tournament_info.game_type = info_json['entities']['event'].get("typeDisplayStr")
	tournament_info.title = info_json['entities']['event'].get("slug")
	tournament_info.url = info_url
	
	
	print "\n---TOURNAMENT INFO---\n", tournament_info
	return tournament_info

# Parse sub_brackets of parent tournaments.
# If the master tournament only has one sub bracket, it will find it in parse_smashgg_info and call this function
def parse_sub_bracket_info(sub_bracket_info, tournament_info):
	sub_bracket_url = sub_bracket_info.url
	
	# in smashgg brackets, sub_bracket for Final Bracket is named '1'
	if sub_bracket_info.name=='1':
		sub_tournament_name = "Final Bracket"
	else:
		sub_tournament_name = sub_bracket_info.name

	full_bracket_name =  tournament_info.name + ' | ' + sub_tournament_name
	print "\n---SUB BRACKET---:", full_bracket_name

	sub_bracket = requests.get(sub_bracket_url)
	sub_bracket_json = sub_bracket.json()
	# pprint(sub_bracket_json)

	# Make call to import_tournament_info using parent tournament info (tournament_info) 
	# Change values for # entrants, url, name
	sub_tournament_info = TournamentInfo(sub_bracket_info.id, full_bracket_name, tournament_info.region, tournament_info.date)
	sub_tournament_info.url = sub_bracket_url
	if sub_bracket_info.name=='1':
		sub_tournament_info.public_url = tournament_info.public_url
	else:
		sub_tournament_info.public_url = tournament_info.public_url + '/' + str(sub_bracket_info.id)

	# Inherited form parent tournament header
	sub_tournament_info.entrants = tournament_info.entrants
	sub_tournament_info.date = tournament_info.date
	sub_tournament_info.parent = tournament_info.name
	sub_tournament_info.game_type = tournament_info.game_type
	print sub_tournament_info

	sub_tournament = import_sub_tournament_info(sub_tournament_info)
	
	entrant_list = parse_bracket_entrants(sub_bracket_json, sub_tournament)
	parse_bracket_sets(sub_bracket_json, entrant_list, sub_tournament)

def parse_bracket_entrants(sub_bracket_json, sub_tournament):
	condensed_entrants = sub_bracket_json['entities']['seeds']
	# pprint(condensed_entrants)

	entrant_list = []
	for entrant in condensed_entrants:
		# pprint(entrant)
		entrant_id = str(entrant.get("entrantId"))
		participant_id = str(entrant['mutations']['entrants'][entrant_id]['participantIds'][0])
		player_id = str(entrant['mutations']['entrants'][entrant_id]['playerIds'][participant_id])
		print entrant_id, participant_id, player_id

		entrant_name = entrant['mutations']['entrants'][entrant_id].get("name")
		entrant_info = EntrantInfo(int(entrant_id), entrant_name)

		# entrant['mutations']['players'][entrant_id] returns list containing one dictionary
		entrant_info.player_tag = entrant['mutations']['players'][player_id].get("gamerTag")
		entrant_info.player_prefix = entrant['mutations']['players'][player_id].get("prefix")
		entrant_info.player_id = entrant['mutations']['players'][player_id].get("id")
		entrant_info.player_region = entrant['mutations']['players'][player_id].get("region")
		entrant_info.player_country = entrant['mutations']['players'][player_id].get("country")
		entrant_info.player_state = entrant['mutations']['players'][player_id].get("state")
		entrant_info.player_sub_seed = entrant.get("groupSeedNum")
		entrant_info.player_super_seed = entrant.get("seedNum")
		entrant_info.player_sub_placing = entrant.get("placement")
		entrant_info.player_super_placing = entrant.get("placement")
		entrant_list.append(entrant_info)

	print "\n---ENTRANTS---"
	for entrant in entrant_list:
		print_ignore(entrant)

	import_tournament_entrants(entrant_list, sub_tournament)
	return entrant_list

# Given JSON of the sub_bracket and list of entrants, isolate sets and record each one individually
def parse_bracket_sets(sub_bracket_json, entrant_list, sub_tournament):
	sets = sub_bracket_json['entities']['sets']
	# pprint(sets)

	set_list = []
	for set in sets:
		set_id = set.get("id")
		set_info = SetInfo(set_id)
		set_info.round_number = set.get("round")
		set_info.round_text = set.get("midRoundText")
		set_info.best_of = set.get("bestOf")

		entrant1Score = set.get("entrant1Score")
		entrant2Score = set.get("entrant2Score")
		if (entrant1Score is None and entrant2Score is None) or (entrant1Score<0 or entrant2Score<0):
			continue

		if set.get("entrant1Id")==set.get("winnerId"):
			set_info.winner_id = set.get("entrant1Id")
			set_info.loser_id = set.get("entrant2Id")
			set_info.winner_score = entrant1Score
			set_info.loser_score = entrant2Score
		else:
			set_info.winner_id = set.get("entrant2Id")
			set_info.loser_id = set.get("entrant1Id")
			set_info.winner_score = entrant2Score
			set_info.loser_score = entrant1Score
		set_info.total_matches = set_info.winner_score + set_info.loser_score

		# Algorithm can be more efficient
		set_info.winner_tag = next((entrant.entrant_name for entrant in entrant_list if set_info.winner_id==entrant.entrant_id), None)
		set_info.loser_tag = next((entrant.entrant_name for entrant in entrant_list if set_info.loser_id==entrant.entrant_id), None)
		set_list.append(set_info)

		# reassign to entrants in import sets
		# set.get('wOverallPlacement')
        # set.get('wPlacement')
	import_tournament_sets(set_list, sub_tournament)


# Given processed tournament_info object parse_tournament_info, add TournamentHeader object to database
def import_tournament_info(tournament_info):
	tournament_game_type = "Super Smash Bros. Melee"

	# if date located in Challonge bracket, use this date, otherwise use date passed in as parameter
	if tournament_info.date is not None:
		tournament_date = tournament_info.date
	else:
		tournament_date = datetime.date(2099, 01, 01)

	new_tournament_header = TournamentHeader(official_title=tournament_info.title,
							host=tournament_info.host,
							public_url=tournament_info.public_url,
							url=tournament_info.url,
							name=tournament_info.name,
							game_type=tournament_game_type,
							date=tournament_date
							)
	db.session.add(new_tournament_header)

	# add tournament_region; if None, then it adds None
	found_region = Region.query.filter(Region.region==tournament_info.region).first()
	new_tournament_header.region = found_region

	db.session.commit()
	return new_tournament_header

def import_sub_tournament_info(sub_tournament_info):
	new_sub_tournament = Tournament(official_title=sub_tournament_info.title,
								url=sub_tournament_info.url,
								public_url=sub_tournament_info.public_url,
								entrants=sub_tournament_info.entrants,
								date=sub_tournament_info.date,
								name=sub_tournament_info.name,
								game_type=sub_tournament_info.game_type
								)

	db.session.add(new_sub_tournament)

	# associate with TournamentHeader
	tournament_header = TournamentHeader.query.filter(TournamentHeader.name==sub_tournament_info.parent).first()
	tournament_header.sub_tournaments.append(new_sub_tournament)
	new_sub_tournament.region = new_sub_tournament.header.region

	db.session.commit()
	print "\n---SUBTOURNAMENT---", new_sub_tournament
	return new_sub_tournament

# Import smashgg entrants and create User objects in database
def import_tournament_entrants(entrant_list, tournament_obj):
	for entrant in entrant_list:
		player_tag = entrant.player_tag
		checked_player = check_set_user(player_tag, tournament_obj.region)

		tournament_obj.placements.append(Placement(
										tournament_id=tournament_obj.id,
										tournament_name=tournament_obj.name,
										user_id=checked_player.id,
										placement=int(entrant.player_sub_placing)
										))
	tournament_obj.entrants = len(entrant_list)
	db.session.commit()
	return tournament_obj

# Import smashgg sets, associate them with Tournament and create Set objects in database
def import_tournament_sets(set_list, sub_tournament):
	print '\n---SETS---'
	for set in set_list:
		print set
		winner_score = set.winner_score
		loser_score = set.loser_score
		total_matches = set.total_matches

		# After calling this function, Users by 'tag' will exist in database in any case.
		# stores User object in respective variables
		set_winner_tag = set.winner_tag.strip()
		winner_user = check_set_user(set_winner_tag, sub_tournament.region)
		set_loser_tag = set.loser_tag.strip()
		loser_user = check_set_user(set_loser_tag, sub_tournament.region)
		round_number = set.round_number

		# Query for associated Tournament
		if sub_tournament.name is not None:
			assocs_tournament = Tournament.query.filter(Tournament.name==sub_tournament.name).first()
		else:
			print "Tournament not Found"

		new_set = Set(tournament_id=assocs_tournament.id,
	                  tournament_name=assocs_tournament.name,
	                  round_type=round_number,
	                  winner_tag=winner_user.tag,
	                  loser_tag=loser_user.tag,
	                  winner_id=winner_user.id,
	                  loser_id=loser_user.id,
	                  winner_score=winner_score,
	                  loser_score=loser_score,
	                  total_matches=total_matches)
		db.session.add(new_set)
		print_ignore(set)

		# update User trueskill ratings based on Set winner and loser
		update_rating(winner_user, loser_user)

	db.session.commit()

# Master function
def parse_bracket_info(tournament_url, tournament_name, tournament_region, tournament_date):
	if tournament_url is None:
		return None
	else:
		# Splice master tournament_id number from the URL (first number after 'brackets/')
		id_start = tournament_url.find("brackets/") + 9
		id_end = tournament_url.find("/", id_start)
		tournament_id = tournament_url[id_start:id_end]

	api_url = "https://api.smash.gg/event/" + tournament_id + "?expand[0]=groups&expand[1]=phase"
	master = requests.get(api_url)
	master_json = master.json()
	# pprint(master_json)
	
	# Process and import tournament info, creating new Tournament object
	tournament_info = parse_tournament_info(tournament_id, tournament_url, tournament_name, tournament_region, tournament_date)
	tournament_obj = import_tournament_info(tournament_info)

	# At this point, master is the JSON showing all the sub_bracket/pool tournaments that are contained within this tournament
	# Subgroup begin at "displayIdentifier", and you want the IDs of each individual sub_bracket.
	# Create list of dictionaries of each sub_bracket with relevant ID info. Only really need "id", to get sub_bracket url
	sub_brackets = master_json['entities']['groups']
	bracket_list = []
	for sub_bracket in sub_brackets:
		sub_bracket_info = SubBracket(sub_bracket.get("id"))
		sub_bracket_info.phase_id = sub_bracket.get("phaseId")
		sub_bracket_info.wave_id = sub_bracket.get("waveId")
		sub_bracket_info.name = sub_bracket.get("displayIdentifier")
		sub_bracket_info.url = "https://api.smash.gg/phase_group/" + str(sub_bracket_info.id) + "?expand%5B%5D=sets&expand%5B%5D=seeds&expand%5B%5D=entrants"
		bracket_list.append(sub_bracket_info)

	for sub_bracket_info in bracket_list:
		parse_sub_bracket_info(sub_bracket_info, tournament_info)

	# Calculate and assign entrants for tournamentHeader
	tournament_header = TournamentHeader.query.filter(TournamentHeader.name==tournament_name).first()
	tournament_header.get_final_entrants()
	print "---FINISHED---"
	return tournament_header