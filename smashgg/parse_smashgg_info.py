import sys
sys.path.insert(0,'..')
sys.path.insert(0,'../sanitize')

from app.models import *
import urllib3
import json
import requests
from pprint import pprint

from parse_challonge_info import import_challonge_info

# Parse sub_brackets of parent tournaments.
# If the master tournament only has one sub bracket, it will find it in parse_smashgg_info and call this function
def parse_sub_bracket_info(sub_bracket_info, tournament_info):
	sub_bracket_url = sub_bracket_info['url']
	sub_bracket_name = sub_bracket_info['name']
	super_bracket_name = tournament_info['name']
	full_bracket_name =  super_bracket_name + ' | ' + sub_bracket_name
	print "\n---SUB BRACKET---:", sub_bracket_url, sub_bracket_name

	sub_bracket = requests.get(sub_bracket_url)
	sub_bracket_json = sub_bracket.json()
	# pprint(sub_bracket_json)

	# Make call to import_challonge_info using parent tournament info (tournament_info) 
	# Change values for # entrants, url, name
	tournament_info['url'] = sub_bracket_url
	sub_tournament = import_challonge_info(tournament_info, full_bracket_name, tournament_info['region'], tournament_info['date'])

	condensed_entrants = sub_bracket_json['entities']['seeds']
	entrant_list = []
	for entrant in condensed_entrants:
		entrant_info = {}
		entrant_info['entrant_id'] = entrant['condensed']['entrant'].get("id")
		entrant_info['entrant_name'] = entrant['condensed']['entrant'].get("name")

		# entrant['condensed']['player'] returns list containing one dictionary
		entrant_info['player_tag'] = entrant['condensed']['player'][0].get("gamerTag")
		entrant_info['player_prefix'] = entrant['condensed']['player'][0].get("prefix")
		entrant_info['player_id'] = entrant['condensed']['player'][0].get("id")
		entrant_info['player_region'] = entrant['condensed']['player'][0].get("region")
		entrant_info['player_country'] = entrant['condensed']['player'][0].get("country")
		entrant_info['player_state'] = entrant['condensed']['player'][0].get("state")
		entrant_info['player_sub_seed'] = entrant.get("groupSeedNum")
		entrant_info['player_sub_placing'] = entrant.get("placement")
		entrant_info['player_super_placing'] = entrant.get("placement")
		entrant_info['player_super_seed'] = entrant.get("seedNum")
		entrant_list.append(entrant_info)

	print "\n---ENTRANTS---"
	for entrant in entrant_list:
		print entrant
		print '\n'

	import_tournament_entrants(entrant_list, sub_tournament)
	parse_bracket_sets(sub_bracket_json, entrant_list)


# Given JSON of the sub_bracket and list of entrants, isolate sets and record each one individually
def parse_bracket_sets(sub_bracket_json, entrant_list):
	sets = sub_bracket_json['entities']['sets']
	set_list = []
	for set in sets:
		set_info = {}
		set_info['round_number'] = set.get("round")
		set_info['round_text'] = set.get("midRoundText")
		set_info['best_of'] = set.get("bestOf")

		entrant1Score = set.get("entrant1Score")
		entrant2Score = set.get("entrant2Score")
		if (entrant1Score is None and entrant2Score is None) or (entrant1Score<0 or entrant2Score<0):
			continue

		if set.get("entrant1Id")==set.get("winnerId"):
			set_info['winner_id'] = set.get("entrant1Id")
			set_info['loser_id'] = set.get("entrant2Id")
			set_info['winner_score'] = entrant1Score
			set_info['loser_score'] = entrant2Score
		else:
			set_info['winner_id'] = set.get("entrant2Id")
			set_info['loser_id'] = set.get("entrant1Id")
			set_info['winner_score'] = entrant2Score
			set_info['loser_score'] = entrant1Score

		# Algorithm can be more efficient
		set_info['winner_tag'] = next((entrant['player_tag'] for entrant in entrant_list if set_info['winner_id']==entrant['entrant_id']), None)
		set_info['loser_tag'] = next((entrant['player_tag'] for entrant in entrant_list if set_info['loser_id']==entrant['entrant_id']), None)
		set_list.append(set_info)

		# reassign to entrants in import sets
		# set.get('wOverallPlacement')
        # set.get('wPlacement')

	print "---SETS---"
	for set in set_list:
		print set

# Gets the base tournament info and stores it in dictionary.
def parse_tournament_info(tournament_id, tournament_name, tournament_region, tournament_date):
	info_url = "https://api.smash.gg/event/" + tournament_id
	info = requests.get(info_url)
	info_json = info.json()
	# pprint(info_json)

	tournament_info = {}
	if info_json['entities']['event'].get("startedAt") is not None:
		tournament_info['date'] = info_json['entities']['event'].get("startedAt")
	else:
		tournament_info['date'] = tournament_date

	tournament_info['id'] = int(tournament_id)
	tournament_info['name'] = tournament_name
	tournament_info['region'] = tournament_region
	tournament_info['game_type'] = info_json['entities']['event'].get("typeDisplayStr")
	tournament_info['title'] = info_json['entities']['event'].get("slug")
	
	print "\n---TOURNAMENT INFO---\n", tournament_info
	return tournament_info

# Eventually, get this tournament id from first number in original url: https://smash.gg/tournament/new-game-plus-49/brackets/12509/26065/85665
# Master function
def parse_bracket_info(tournament_url, tournament_name, tournament_region, tournament_date):
	if tournament_url is None:
		return None
	else:
		# Splice master tournament_id number from the URL (first number after 'brackets/')
		id_start = tournament_url.find("brackets/") + 9
		id_end = tournament_url.find("/", id_start)
		tournament_id = tournament_url[id_start:id_end]

	tournament_url = "https://api.smash.gg/event/" + tournament_id + "?expand[0]=groups&expand[1]=phase"
	master = requests.get(tournament_url)
	master_json = master.json()
	# pprint(master_json)
	
	# Process and import tournament info, creating new Tournament object
	tournament_info = parse_tournament_info(tournament_id, tournament_name, tournament_region, tournament_date)
	tournament_obj = import_challonge_info(tournament_info, tournament_name, tournament_region, tournament_date)

	# At this point, master is the JSON showing all the sub_bracket/pool tournaments that are contained within this tournament
	# Subgroup begin at "displayIdentifier", and you want the IDs of each individual sub_bracket.
	# Create list of dictionaries of each sub_bracket with relevant ID info. Only really need "id", to get sub_bracket url
	sub_brackets = master_json['entities']['groups']
	bracket_list = []
	for sub_bracket in sub_brackets:
		sub_bracket_info = {}
		sub_bracket_info["id"] = sub_bracket.get("id")
		sub_bracket_info["phase_id"] = sub_bracket.get("phaseId")
		sub_bracket_info["wave_id"] = sub_bracket.get("waveId")
		sub_bracket_info["name"] = sub_bracket.get("displayIdentifier")
		print "displayIdentifier:", sub_bracket_info["name"]
		sub_bracket_info["url"] = "https://api.smash.gg/phase_group/" + str(sub_bracket.get("id")) + "?expand%5B%5D=sets&expand%5B%5D=seeds&expand%5B%5D=entrants"
		bracket_list.append(sub_bracket_info)

	for sub_bracket in bracket_list:
		parse_sub_bracket_info(sub_bracket, tournament_info)


# Import smashgg entrants and create User objects
def import_tournament_entrants(entrant_list, tournament_obj):
	for entrant in entrant_list:
		player_tag = entrant['player_tag']

		if tournament_obj.region:
			checked_player = check_set_user(player_tag, tournament_obj.region.region)
		else:
			checked_player = check_set_user(player_tag)

		tournament_obj.placements.append(Placement(
										tournament_id=tournament_obj.id,
										tournament_name=tournament_obj.name,
										user_id=checked_player.id,
										placement=int(entrant['player_sub_placing'])
										))

	db.session.commit()
	return tournament_obj