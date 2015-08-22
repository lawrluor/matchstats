#!flask/bin/python

from app import app, db
from app.models import *

import urllib3
from bs4 import BeautifulSoup

import sys
import unicodedata

from parse_challonge_standings import *
from parse_challonge_info import *
from parse_challonge_matches import *

def main():
  tournament_url = sys.argv[1]
  tournament_name = sys.argv[2]  
  tournament_region = sys.argv[3]
  tournament_date = sys.argv[4]

  # Check for region, if not specific Region, set to None
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

if __name__ == "__main__":
	main()

# This function is identical to main, but can be called outside of the terminal (namely in parse_challonge_tournamentlist.py, which adds Challonge tournaments to the database given a text file list of Challonge tournaments.
def parse_challonge_run(tournament_url, tournament_name, tournament_region, tournament_date):
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

def parse_challonge_pool(pool_url, parent_tournament_name, tournament_region, advance_number):
  # Query to find parent tournament (Final Bracket Tournament) by name
  parent_tournament = Tournament.query.filter(Tournament.name==parent_tournament_name).first()
  pool_placements = parse_pool_standings(pool_url, tournament_region, advance_number)
  import_pool_standings(pool_placements, parent_tournament)

  matchlist = parse_challonge_matches(pool_url, tournament_region)
  import_challonge_matches(matchlist, parent_tournament.name, tournament_region, True)
