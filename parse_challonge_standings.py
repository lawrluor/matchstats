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
    print player_rows[i] 
    print '\n'

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
     
    print standing
    print tag
    print '\n'

  print all_placements
  return all_placements


def parse_challonge_info(tournament_url):
  conn3 = urllib3.connection_from_url(tournament_url)
  r3 = conn3.request("GET", tournament_url)
  soup3 = BeautifulSoup(r3.data)
  soup3.prettify()

  found = soup3.find_all("meta") 
  print found

