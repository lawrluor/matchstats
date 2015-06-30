#!flask/bin/python
# Currently supports: fully loaded Challonge Bracket with: seed or no seed displayed, score=int or \xe2\x9c\x93 (checkmark) unicode, data-round=int, <span> title=str
# Note: Challonge refers to Sets as "match". I will adopt the term "match" to represent Set only in this file, for the sake of simplicity.

import urllib3
from bs4 import BeautifulSoup
import re

# Given list of top_match_half items, parse lines to get relevant data for round, tag, seed, and score
def parse_top_match(tag_list):
  for tag in tag_list:
    match_round = str(tag.find_all("div", {"class" : "inner_content"}))
    span_tag = str(tag.find("span")) 
    div_seed = str(tag.find_all("div", {"class" : "top_seed"}))
    div_score = str(tag.find_all("div", {"class" : "top_score"}))

    # dictionary which will contain relevant data
    top_half = {}

    if match_round and len(match_round) > 2:
      start_text = "data-round=\""
      end_text = "\"><"

      start_index = match_round.find(start_text) + 12
      end_index = match_round.find(end_text)
      top_half["round"] = match_round[start_index:end_index]

    if span_tag and len(span_tag) > 0:
      processed_span_tag = '~' + span_tag[1:]
      start_index = processed_span_tag.index('>') + 1
      end_index = processed_span_tag.index('<')
      top_half["tag"] = processed_span_tag[start_index:end_index]
    
    if div_seed and len(div_seed) > 2:
      processed_div_seed = '~' + div_seed[2:]
      start_index = processed_div_seed.index('>') + 1
      end_index = processed_div_seed.index('<')
      top_half["seed"] = processed_div_seed[start_index:end_index]


    if div_score and len(div_score) > 2:
      processed_div_score = '~' + div_score[2:] 
      start_index = processed_div_score.index('>') + 1
      end_index = processed_div_score.index('<') 
      # Check for alternate win scores: checkmark Unicode character, empty score
      if processed_div_score[start_index:end_index] == "\xe2\x9c\x93":
        top_half["score"] = 1
      elif processed_div_score[start_index:end_index] == '':
        top_half["score"] = 0
      else:
        top_half["score"] = 0

    return top_half

# given list of bottom_half items, parse lines to get relevant data for round, tag, seed, and score
def parse_bottom_match(tag_list):
  for tag in tag_list:
    match_round = str(tag.find_all("div", {"class" : "inner_content"}))
    span_tag = str(tag.find("span")) 
    div_seed = str(tag.find_all("div", {"class" : "bottom_seed"}))
    div_score = str(tag.find_all("div", {"class" : "bottom_score"}))

    # dictionary containing relevant data to be returned
    bottom_half  = {}
    
    if match_round and len(match_round) > 2:
      start_text = "data-round=\""
      end_text = "\"><"

      start_index = match_round.find(start_text) + 12
      end_index = match_round.find(end_text)
      bottom_half["round"] = match_round[start_index:end_index]

    if span_tag and len(span_tag) > 0:
      processed_span_tag = '~' + span_tag[1:]
      start_index = processed_span_tag.index('>') + 1
      end_index = processed_span_tag.index('<')
      bottom_half["tag"] = span_tag[start_index:end_index]
    
    if div_seed and len(div_seed) > 2:
      processed_div_seed = '~' + div_seed[2:]
      start_index = processed_div_seed.index('>') + 1
      end_index = processed_div_seed.index('<')
      bottom_half["seed"] = processed_div_seed[start_index:end_index]

    if div_score and len(div_score) > 2:
      processed_div_score = '~' + div_score[2:] 
      start_index = processed_div_score.index('>') + 1
      end_index = processed_div_score.index('<') 
      # Check for alternate win scores: checkmark Unicode character, empty score
      if processed_div_score[start_index:end_index] == "\xe2\x9c\x93":
        bottom_half["score"] = 1
      elif processed_div_score[start_index:end_index] == '':
        bottom_half["score"] = 0
      else:
        bottom_half["score"] = 0

    return bottom_half

# currently grabbing from: CEO 2014 Top 32 Bracket
Tournament = "http://ceogaming.challonge.com/ceo2014ssbmtop32"
conn = urllib3.connection_from_url(Tournament)
r1 = conn.request("GET", Tournament)
soup = BeautifulSoup(r1.data)
soup.prettify()

# find all matches
# first line identifying a match: <td class='core' id='match_qtip_23317245_' style='padding:0'>
all_matches = soup.find_all("td", {"class" : "core"}, id=re.compile("\S"))
for match in all_matches:
  print str(match)
  print '\n'
print "done printing all_matches"
print '\n'

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
  if top_half['round'] != None:    
    round_num = matches_by_round.setdefault(top_half['round'], [])
    round_num.append(top_half)

  match_bottom = div_tag.find_all("div", {"class" : "match_bottom_half"})
  # pass list containing all match_bottom_half to parse_bottom_match, which will parse lines separately for data
  bottom_half = parse_bottom_match(match_bottom)
  # append dictionary from bottom_half into the same inner list as top_half. This is one dictionary representing the bottom_half
  current_match.append(bottom_half)
  print bottom_half

  # add match half to dictionary by round; if no key exists for round, create one
  if bottom_half['round'] != None:    
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
