#!flask/bin/python

import sys
sys.path.append('./sanitize')

from sanitize_utils import check_and_sanitize_tag
from app.models import *

import urllib3
from bs4 import BeautifulSoup
import re
import collections

# Second soup for parsing Standings (placements)
def parse_challonge_standings(tournament_url, tournament_region): 
  # find /standings page given tournament bracket url
  standings_url = tournament_url + '/standings'

  conn2 = urllib3.connection_from_url(standings_url)
  r2 = conn2.request("GET", standings_url)
  soup2 = BeautifulSoup(r2.data)
  soup2.prettify()

  player_rows = soup2.find_all("tr")
  # OrderedDict so that keys are remembered in the order they come in, from least to greatest.
  all_placements = collections.OrderedDict()
  current_placement = 0
  for i in range(1, len(player_rows)):
    standing_item = player_rows[i].find("td", {"class" : "rank"})
    if standing_item is not None:
      current_placement = int(standing_item.getText())
      standing = current_placement
    else:
      standing = current_placement

    tag_item = player_rows[i].find("span")
    if tag_item is not None:
      tag = tag_item.getText()
      # "Advanced" text is unwanted, non-tag information
      if tag == "Advanced":
        continue
      tag = tag.strip('\n')
      
      sanitized_tag = check_and_sanitize_tag(tag, tournament_region)

    # limit number of Users who can tie for a placement
    placing = all_placements.setdefault(standing, [])
    if len(all_placements[standing]) < standing_limit(standing):
      placing.append(sanitized_tag)
     
  print "PLACEMENTS:", all_placements.items()
  print '\n'
  return all_placements


# given all_placements dictionary from parse_challonge_standings, and a Tournament object created in import_challonge_info, add placements data to Tournament object.
def import_challonge_standings(all_placements, tournament):
  for placement in all_placements:
    for player in all_placements[placement]:
      # check or create new User object, tag=player
      if tournament.region is not None:
        checked_player = check_set_user(player, tournament.region.region)
      else:
        checked_player = check_set_user(player)
      
      # append relationship to Tournament as a Placement object; Placement objects are appended into a list in order of their User id, with no relation to their placing or tag.
      tournament.placements.append(Placement(tournament_id=tournament.id,
                                        tournament_name=tournament.name,
                                        user_id=checked_player.id,
                                        placement=placement
                                        ))
  db.session.commit()
  return tournament

# Establishes limit for number of Users who can tie for a placement; limit only relevant for Double Elimination brackets
def standing_limit(standing):
  base_limit = 2
  if standing < 5:
    limit = 1
  elif standing==5 or standing==7:
    limit = 2
  elif standing==9 or standing==13:
    limit = 4
  elif standing==17 or standing==25:
    limit = 8
  elif standing==33 or standing==49:
    limit = 16
  elif standing==65 or standing==97:
    limit = 32
  elif standing==129 or standing==193:
    limit = 64
  elif standing==257 or standing==385:
    limit = 128
  elif standing==513 or standing==769:
    limit = 256
  elif standing==1025 or standing==1537:
    limit = 512
  elif standing==2049 or standing==3037:
    limit = 1024
  else:
    limit = sys.maxint
  return limit
     
