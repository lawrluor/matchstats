#!flask/bin/python
# Currently supports: fully loaded Challonge Bracket with: seed or no seed displayed, score=int or \xe2\x9c\x93 (checkmark) unicode, data-round=int, <span> title=str
# Note: Challonge refers to Sets as "match". I will adopt the term "match" to represent Set only in this file, for the sake of simplicity.

from app.models import *
import sys
sys.path.append('./sanitize')
from sanitize_utils import check_and_sanitize_tag

import urllib3
from bs4 import BeautifulSoup
import re

# Given list of top_match_half items, parse lines to get relevant data for round, tag, seed, and score
def parse_top_match(top_item_list):
  # dictionary which will contain relevant data
  top_half = {}

  for item in top_item_list:
    round_item = item.find("div", {"class" : "inner_content"})
    round_number = round_item["data-round"]
    if round_number:
      top_half["round"] = int(round_number)

    span_item = item.find("span")
    tag = span_item.getText()
    if tag:
      top_half["tag"] = check_and_sanitize_tag(tag)

    seed_item = item.find("div", {"class" : "top_seed"})
    if seed_item is not None:
      seed_number = seed_item.getText()
      top_half["seed"] = int(seed_number)
      
    score_item = item.find("div", {"class" : "top_score"})
    score = score_item.string
    if score:
      if score == u"\u2713":
        top_half["score"] = 1 
      elif score == "":
        top_half["score"] = 0
      else:
        top_half["score"] = int(score)
    else:
      top_half["score"] = 0

    return top_half

# Given list of top_match_half items, parse lines to get relevant data for round, tag, seed, and score
def parse_bottom_match(bottom_item_list):
  # dictionary which will contain relevant data
  bottom_half = {}

  for item in bottom_item_list:
    round_item = item.find("div", {"class" : "inner_content"})
    round_number = round_item['data-round']
    if round_number:
      bottom_half["round"] = int(round_number)

    span_item = item.find("span")
    tag = span_item.getText()
    if tag:
      bottom_half["tag"] = check_and_sanitize_tag(tag)

    seed_item = item.find("div", {"class" : "bottom_seed"})
    if seed_item is not None:
      seed_number = seed_item.getText()
      bottom_half["seed"] = int(seed_number)
      
    score_item = item.find("div", {"class" : "bottom_score"})
    score = score_item.string
    if score:
      if score == u"\u2713":
        bottom_half["score"] = 1 
      elif score == "":
        bottom_half["score"] = 0
      else:
        bottom_half["score"] = int(score)
    else:
      bottom_half["score"] = 0

    return bottom_half

def parse_challonge_matches(tournament_url):
  conn = urllib3.connection_from_url(tournament_url)
  r1 = conn.request("GET", tournament_url)
  soup = BeautifulSoup(r1.data)
  soup.prettify()

  # find all matches
  # first line identifying a match: <td class='core' id='match_qtip_23317245_' style='padding:0'>
  all_matches = soup.find_all("td", {"class" : "core"}, id=re.compile("\S"))

  # a dictionary that stores match information by round number. Each dictionary key represents a round number in winners or losers side of the bracket. As per Challonge, -1 = losers round 1, while 1 = winners round 1
  matches_by_round = {}
  # a list of lists of pairs of dictionaries. The dictionary pair represents a match, with top_half and bottom_half data stored in the inner list index 0 and 1 respectively. The outer list contains each match representation, iterable by index.
  matchlist = []

  for div_tag in all_matches:
    # create inner list, to store the two dictionaries that represent a match
    current_match = []

    match_top = div_tag.find_all("div", {"class" : "match_top_half"})
    # pass list containing all match_top_half to parse_top_match, which will parse lines separately for data
    top_half = parse_top_match(match_top)
    # append dictionary from parse_top_match into the inner list. This is one dictionary representing the top_half
    current_match.append(top_half)
    print top_half

    # add match half to dictionary by round; if no key exists for round, create one
    if top_half['round'] is not None:    
      round_num = matches_by_round.setdefault(top_half['round'], [])
      round_num.append(top_half)

    match_bottom = div_tag.find_all("div", {"class" : "match_bottom_half"})
    # pass list containing all match_bottom_half to parse_bottom_match, which will parse lines separately for data
    bottom_half = parse_bottom_match(match_bottom)
    # append dictionary from bottom_half into the same inner list as top_half. This is one dictionary representing the bottom_half
    current_match.append(bottom_half)
    print bottom_half

    # add match half to dictionary by round; if no key exists for round, create one
    if bottom_half['round'] is not None:    
      round_num = matches_by_round.setdefault(top_half['round'], [])
      round_num.append(bottom_half)
    
    print current_match
    # append the inner list representing this match to the outer list, which will eventually contain all matches in the bracket.
    matchlist.append(current_match)
    print '\n'

  print matches_by_round
  print '\n'
  for match in matchlist:
    print match
  print '\n'

  return matchlist


# Get: score, tag, seed, round given a matchlist from parse_challonge, and a string tournamnent name (to fill out Set.attribute)
def import_challonge_matches(matchlist, tournament_name):
  for set in matchlist:
    top_player = set[0]
    bottom_player = set[1]

    # Determine the set winner and loser based on their scores. Once assigned, no more references 
    # will be made to the ambiguous top and bottom player, but instead to set_winner and set_loser
    # Both set_winner and set_loser are DICTIONARIES. Scores are stored in respective variables

    # check scores; if either score is a DQ score, break and don't store set 
    if top_player['score']==-1 or bottom_player['score']==-1:
      print "DQ SCORE DETECTED" + '\n'
      continue

    if top_player['score'] > bottom_player['score']:
      set_winner = top_player
      set_loser = bottom_player
      winner_score = top_player['score']
      loser_score = bottom_player['score']
    else:
      set_winner = bottom_player
      set_loser = top_player
      winner_score = bottom_player['score']
      loser_score = top_player['score']

    # After calling this function, Users by 'tag' will exist in database in any case.
    # stores User object in respective variables
    winner_user = check_set_user(set_winner['tag'])
    loser_user = check_set_user(set_loser['tag'])

    # If seed doesn't exist, do nothing; else, assign to User attribute seed
    if 'seed' in set_winner:
      winner_user.seed = set_winner['seed']
    if 'seed' in set_loser:
      loser_user.seed = set_loser['seed']

    # Get round number; if they match, store the round variable; if they don't (some error occurred), ignore it.
    if int(set_winner['round']) == int(set_loser['round']):
      round_number = int(set_winner['round'])
    else:
      # prevent crashing when creating the Set without existing variable round_number
      round_number = 0

    # get associated Tournament
    if tournament_name is not None:
      assocs_tournament = Tournament.query.filter(Tournament.name==tournament_name).first()
    else:
      # Default Tournament object "Non-Tourney", id=1
      assocs_tournament = Tournament.query.filter(Tournament.name=="Non-Tourney").first()

    new_set = Set(tournament_id=assocs_tournament.id,
                  tournament_name=assocs_tournament.name,
                  round_type=round_number,
                  winner_tag=winner_user.tag,
                  loser_tag=loser_user.tag,
                  winner_id=winner_user.id,
                  loser_id=loser_user.id,
                  winner_score=winner_score,
                  loser_score=loser_score,
                  total_matches=winner_score+loser_score)

    db.session.add(new_set)
    print new_set

  db.session.commit()
  print '\n'

  return "Import Successful"
