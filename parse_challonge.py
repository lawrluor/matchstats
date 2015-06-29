#!flask/bin/python

import urllib3
from bs4 import BeautifulSoup

def parse_top_match(div_list):
  for tag in match_top:
    match_round = str(div_tag.find_all("div", {"class" : "inner_content"}))
    div_score = str(tag.find_all("div", {"class" : "top_score"}))
    div_seed = str(tag.find_all("div", {"class" : "top_seed"}))
    span_tag = str(tag.find("span")) 

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

    if div_score and len(div_score) > 2:
      processed_div_score = '~' + div_score[2:] 
      start_index = processed_div_score.index('>') + 1
      end_index = processed_div_score.index('<') 
      top_half["score"] = processed_div_score[start_index:end_index]
    
    if div_seed and len(div_seed) > 2:
      processed_div_seed = '~' + div_seed[2:]
      start_index = processed_div_seed.index('>') + 1
      end_index = processed_div_seed.index('<')
      top_half["seed"] = processed_div_seed[start_index:end_index]

    return top_half

def parse_bottom_match(div_list):
  for tag in match_bottom:
    match_round = str(div_tag.find_all("div", {"class" : "inner_content"}))
    div_score = str(tag.find_all("div", {"class" : "bottom_score"}))
    div_seed = str(tag.find_all("div", {"class" : "bottom_seed"}))
    span_tag = str(tag.find("span")) 

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

    if div_score and len(div_score) > 2:
      processed_div_score = '~' + div_score[2:] 
      start_index = processed_div_score.index('>') + 1
      end_index = processed_div_score.index('<') 
      bottom_half["score"] = processed_div_score[start_index:end_index]
    
    if div_seed and len(div_seed) > 2:
      processed_div_seed = '~' + div_seed[2:]
      start_index = processed_div_seed.index('>') + 1
      end_index = processed_div_seed.index('<')
      bottom_half["seed"] = processed_div_seed[start_index:end_index]

    return bottom_half

conn = urllib3.connection_from_url("http://challonge.com/apex2014meleesinglestop8") 
r1 = conn.request("GET", "http://challonge.com/apex2014meleesinglestop8")
soup = BeautifulSoup(r1.data)
soup.prettify()

all_sets = soup.find_all("td", {"class" : "core"})
for set in all_sets:
  print str(set)
  print '\n'
print "done printing all_sets"
print '\n'

setlist = []
for div_tag in all_sets:

  match_top = div_tag.find_all("div", {"class" : "match_top_half"})
  top_half = parse_top_match(match_top)
  print top_half
  setlist.append(top_half)

  match_bottom = div_tag.find_all("div", {"class" : "match_bottom_half"})
  bottom_half = parse_bottom_match(match_bottom)
  print bottom_half
  
  print '\n'
