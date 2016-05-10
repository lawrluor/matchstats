#!flask/bin/python

from app import app, db
from app.models import *

import urllib3
from bs4 import BeautifulSoup

import sys
import unicodedata

sys.path.insert(0, './parsers')
from parse_smashgg_info import *
from challonge_parse import *

# Helper function for read_tournamentlist
# Parses relevant info regarding a tournament given string containing tournament name, url, region, and date
# New\ Game\ Plus\ 1|http://bigbluees.challonge.com/NGP1|04/28/2015 
# Returns: dictionary with relevant keywords attaced to values
def process_tournament_line(tournament_line, region):
  # process each line and parse tournament_url, tournament_name 
  processed_tournament_line = tournament_line.strip('\n')
  line_parser = re.compile('[|]')
  tokens = line_parser.split(processed_tournament_line)
  tournament_name = tokens[0]
  # Remove '\' escape characters
  tournament_name = tournament_name.translate(None, '\\')

  tournament_url = tokens[1]
  tournament_date = tokens[2]
  
  # If region passed as string "None", "Global", convert to None object
  if region=="None" or region=="Global":
    tournament_region = None
  else:
    tournament_region = region.translate(None, '\\')

  # Diffrentiate whether given tournament is a Smashgg or Challonge bracket. Hacky
  if "challonge" in tournament_url:
    challonge.set_credentials("ssbtonic", "55TSSgywjR2bPpvIXDMrm5pZ6edm6Iq0rmcCXK5c")
    process_tournament(tournament_url, tournament_name, tournament_region, tournament_date)
  elif "smash.gg" in tournament_url:
    parse_bracket_info(tournament_url, tournament_name, tournament_region, tournament_date)
  else:
    return "Bracket system not recognized"
  
  print tournament_url, tournament_name, tournament_region, tournament_date



# ---DEPERECATED---
# Takes parameter String tournament_line, a block of tournament info
# Runs functions to add Tournament to database
# "New\ Game\ Plus\ 1|http://bigbluees.challonge.com/NGP1|New\ England|04/28/2015"
# Returns None
def parse_challonge_run(tournament_line):
  # Parse the tournament_line, and assign values to local vars
  tournament_info = process_tournament_line(tournament_line)
  tournament_name = tournament_info['tournament_name']
  tournament_url = tournament_info['tournament_url']
  tournament_region = tournament_info['tournament_region']
  tournament_date = tournament_info['tournament_date']

  if tournament_region=="None" or tournament_region=="Global" or tournament_region=="National":
    tournament_region = None

  # Convert passed parameter date to datetime object if not None
  if tournament_date!="None":
    tournament_date = convert_int_date(tournament_date)
  else:
    tournament_date = None

  # Create and return dictionary of values for Tournament attributes
  tournament_info = parse_challonge_info(tournament_url)
  # create new Tournament by assigning the tournament_info dictionary, given the tournament name as well.
  new_tourney = import_challonge_info(tournament_info, tournament_name, tournament_url, tournament_region, tournament_date)
 
  # Returns dictionary of placements : tags given tournament url
  all_placements = parse_challonge_standings(tournament_url, tournament_region)
  # given the dictionary of placements and the Tournament object, link Tournament and User with Placement object. Users checked and sanitized here.
  import_challonge_standings(all_placements, new_tourney)

  # given the tournament_url, return a list of dictionaries with values for Set attributes
  matchlist = parse_challonge_matches(tournament_url, tournament_region)
  # Create Set objects with matchlist, and append them to the relationship between Tournament and Sets
  import_challonge_matches(matchlist, tournament_name, tournament_region, False)

def main():
  tournament_line = sys.argv[1]
  parse_challonge_run(tournament_line)

if __name__ == "__main__":
	main()

def parse_challonge_pool(pool_url, parent_tournament_name, tournament_region, advance_number):
  # Query to find parent tournament (Final Bracket Tournament) by name
  parent_tournament = Tournament.query.filter(Tournament.name==parent_tournament_name).first()
  pool_placements = parse_pool_standings(pool_url, tournament_region, advance_number)
  import_pool_standings(pool_placements, parent_tournament)

  matchlist = parse_challonge_matches(pool_url, tournament_region)
  import_challonge_matches(matchlist, parent_tournament.name, tournament_region, True)

# This function is obsolete, takes in tournament info in different format. 
def parse_challonge_run_alt(tournament_url, tournament_name, tournament_region, tournament_date):
  if tournament_region=="None" or tournament_region=="Global" or tournament_region=="National":
    tournament_region = None

  # Convert passed parameter date to datetime object if not None
  if tournament_date!="None":
    tournament_date = convert_int_date(tournament_date)
  else:
    tournament_date = None

  # Create and return dictionary of values for Tournament attributes
  tournament_info = parse_challonge_info(tournament_url)
  # create new Tournament by assigning the tournament_info dictionary, given the tournament name as well.
  new_tourney = import_challonge_info(tournament_info, tournament_name, tournament_url, tournament_region, tournament_date)
 
  # Returns dictionary of placements : tags given tournament url
  all_placements = parse_challonge_standings(tournament_url, tournament_region)
  # given the dictionary of placements and the Tournament object, link Tournament and User with Placement object. Users checked and sanitized here.
  import_challonge_standings(all_placements, new_tourney)

  # given the tournament_url, return a list of dictionaries with values for Set attributes
  matchlist = parse_challonge_matches(tournament_url, tournament_region)
  # Create Set objects with matchlist, and append them to the relationship between Tournament and Sets
  import_challonge_matches(matchlist, tournament_name, tournament_region, False)
