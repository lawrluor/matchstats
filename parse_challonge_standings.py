#!flask/bin/python

from app.models import *
import sys
sys.path.append('./sanitize')
from sanitize_utils import check_and_sanitize_tag

import urllib3
from bs4 import BeautifulSoup
import re

# Second soup for parsing Standings (placements)
def parse_challonge_standings(tournament_url): 
  # find /standings page given tournament bracket url
  standings_url = tournament_url + '/standings'

  conn2 = urllib3.connection_from_url(standings_url)
  r2 = conn2.request("GET", standings_url)
  soup2 = BeautifulSoup(r2.data)
  soup2.prettify()

  player_rows = soup2.find_all("tr")

  all_placements = {}
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

    placing = all_placements.setdefault(standing, [])
    placing.append(tag)
     
  print all_placements
  print '\n'
  return all_placements


# given all_placements dictionary from parse_challonge_standings, and a Tournament object created in import_challonge_info, add placements data to Tournament object.
def import_challonge_standings(all_placements, tournament):
  for placement in all_placements:
    for player in all_placements[placement]:
      # checked_player is a User object
      checked_player = check_set_user(player)
      checked_player.tag = check_and_sanitize_tag(checked_player.tag)
      
      # append relationship to Tournament as a Placement object
      tournament.users.append(Placement(tournament_id = tournament.id,
                                        user_id=checked_player.id,
                                        placement=placement
                                        ))
  db.session.commit()
  return tournament
