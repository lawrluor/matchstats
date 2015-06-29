#!flask/bin/python

import urllib3
from bs4 import BeautifulSoup
import re

def parse_top_match(tag_list):
  for tag in tag_list:
    match_round = str(tag.find_all("div", {"class" : "inner_content"}))
    span_tag = str(tag.find("span")) 
    div_seed = str(tag.find_all("div", {"class" : "top_seed"}))
    div_score = str(tag.find_all("div", {"class" : "top_score"}))

    top_half = {}

    if match_round and len(match_round) > 2:
      winners_round_text = "data-round=\""
      losers_round_text = "data-round=\"-"

      if match_round.find(losers_round_text) == -1:
        start_index = match_round.find(winners_round_text) + 12
        end_index = start_index + 1
        top_half["round"] = match_round[start_index:end_index]
      else:
        start_index = match_round.find(losers_round_text) + 12
        end_index = start_index + 2
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
      top_half["score"] = processed_div_score[start_index:end_index]

    return top_half

def parse_bottom_match(tag_list):
  for tag in tag_list:
    match_round = str(tag.find_all("div", {"class" : "inner_content"}))
    span_tag = str(tag.find("span")) 
    div_seed = str(tag.find_all("div", {"class" : "bottom_seed"}))
    div_score = str(tag.find_all("div", {"class" : "bottom_score"}))

    bottom_half  = {}
    
    if match_round and len(match_round) > 2:
      winners_round_text = "data-round=\""
      losers_round_text = "data-round=\"-"

      if match_round.find(losers_round_text) == -1:
        start_index = match_round.find(winners_round_text) + 12
        end_index = start_index + 1
        bottom_half["round"] = match_round[start_index:end_index]
      else:
        start_index = match_round.find(losers_round_text) + 12
        end_index = start_index + 2
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
      bottom_half["score"] = processed_div_score[start_index:end_index]

    return bottom_half

conn = urllib3.connection_from_url("http://challonge.com/apex2014meleesinglestop8") 
r1 = conn.request("GET", "http://challonge.com/apex2014meleesinglestop8")
soup = BeautifulSoup(r1.data)
soup.prettify()

"""
match_top = soup.find_all("div", {"class" : "match_top_half"})
top_half = parse_top_match(match_top)
print top_half
print '\n'

match_bottom = soup.find_all("div", {"class" : "match_bottom_half"})
bottom_half = parse_bottom_match(tag)
print bottom_half
"""

all_sets = soup.find_all("td", {"class" : "core"}, id=re.compile("\S"))
for set in all_sets:
  print str(set)
  print '\n'
print "done printing all_sets"
print '\n'

sets_by_round = {}
setlist = []
for div_tag in all_sets:
  current_set = []

  match_top = div_tag.find_all("div", {"class" : "match_top_half"})
  top_half = parse_top_match(match_top)
  current_set.append(top_half)
  print top_half

  if top_half['round'] != None:    
    round_num = sets_by_round.setdefault(top_half['round'], [])
    round_num.append(top_half)

  match_bottom = div_tag.find_all("div", {"class" : "match_bottom_half"})
  bottom_half = parse_bottom_match(match_bottom)
  current_set.append(bottom_half)
  print bottom_half

  if top_half['round'] != None:    
    round_num = sets_by_round.setdefault(top_half['round'], [])
    round_num.append(top_half)
  
  print current_set
  setlist.append(current_set)
  print '\n'

print sets_by_round
print '\n'
for set in setlist:
  print set
