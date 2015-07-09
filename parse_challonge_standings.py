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
  print '\n'

  return all_placements

# given all_placements dictionary from parse_challonge_standings, and a Tournament object created in import_challonge_info, add placements data to Tournament object.
def import_challonge_standings(all_placements, tournament):
  for placement in all_placements:
    for player in all_placements[placement]:
      # checked_player is a User object
      checked_player = check_set_user(player)
      
      # append relationship to Tournament as a Placement object
      tournament.users.append(Placement(tournament_id = tournament.id,
                                        user_id=checked_player.id,
                                        placement=placement
                                        ))
      db.session.commit()

  # query Tournaments to see
  placements = db.session.query(Tournament).join('users', 'user')

  print tournament
  print tournament.name

# function for parsing tournament general info given a Challonge bracket
def parse_challonge_info(tournament_url):
  conn3 = urllib3.connection_from_url(tournament_url)
  r3 = conn3.request("GET", tournament_url)
  soup3 = BeautifulSoup(r3.data)
  soup3.prettify()

  tournament_info = {}

  title_item = soup3.find("div", id='title') 
  if title_item is not None:
    title = title_item.getText()
    title = title.strip('\n')
    tournament_info['title'] = title
    print title
  print '\n'

  host_item = soup3.find("div", {"class" : "text"})
  if host_item is not None:
    # text is a string containing a string, i.e. "Hosted by CEO Gaming"
    text = host_item.getText()
    host_index = text.find("by")
    if host_index != -1:
      # use index when "host" starts, host_index, and account for the word and whitespace to get everything after "by "
      host = text[host_index+2:]
    else:
      host = text
    
    host = host.strip('\n')
    tournament_info['host'] = host
    print host
  print '\n'

  game_type_item = soup3.find("a", {"href" : re.compile('http://challonge.com/games/.*')})
  if game_type_item is not None:
    game_type = game_type_item.getText()
    game_type = game_type.strip('\n')
    tournament_info['game_type'] = game_type
    print game_type
  print '\n'

  date_item = soup3.find("span", id='start-time') 
  if date_item is not None:
    full_date = date_item.getText()
    # full_date is a string, i.e. "June 27, 2015 at 6:00 PM EDT". This will be truncated to just the month, day, and year
    date_index = full_date.find("at")
    if date_index != -1:
      date = full_date[:(date_index-1)] 
    else:
      date = full_date

    date = date.strip('\n')
    tournament_info['date'] = date
    print date
  print '\n'
  
  # locates an info icon near the bracket type description, because the bracket_type description does not exist inside a tag
  bracket_locator = soup3.find("i", {"class" : "icon-info-sign"})
  if bracket_locator is not None:
    # next line happens to contain a string with the bracket information and entrant number, i.e. "32 player Double Elimination"
    bracket_info = bracket_locator.nextSibling
    print bracket_info

    # find start index for player, subtract 1 (whitespace) to get just the number of entrants "32" and convert to int
    player_index = bracket_info.find("player") 
    if player_index != -1:
      entrants = int(bracket_info[:(player_index-1)])
      # use index when "player" starts, player_index, and account for the word and whitespace to get everything after "player "
      bracket_type = bracket_info[(player_index+7):].strip('\n')
    else:
      entrants = bracket_info.strip('\n')
      bracket_type = bracket_info.strip('\n')

    tournament_info['entrants'] = entrants
    tournament_info['bracket_type'] = bracket_type
    print entrants
    print bracket_type
  print '\n'

  print tournament_info
  return tournament_info

# get tourney title, host, number of entrants, bracket type, game type, and date given an info dictionary from parse_challonge_info, and a string tournament_name, and create and return a Tournament object
def import_challonge_info(tournament_info, tournament_name):
  print tournament_info
  
  if 'title' in tournament_info:
    tournament_title = tournament_info['title']
  else:
    tournamemnt_title = None
  
  if 'host' in tournament_info:
    tournament_host = tournament_info['host']
  else:
    tournament_host = None

  if 'entrants' in tournament_info:
    tournament_entrants = tournament_info['entrants']
  else:
    tournament_entrants = None

  if 'bracket_type' in tournament_info:
    tournament_bracket_type = tournament_info['bracket_type']
  else:
    tournament_bracket_type = None

  if 'game_type' in tournament_info:
    tournament_game_type = tournament_info['game_type']
  else:
    tournament_game_type = None

  if 'date' in tournament_info:
    tournament_date = tournament_info['date']
  else:
    tournament_date = None

  if tournament_name is None:
    tournament_name = "Non-Tourney"
 
  new_tournament = Tournament(official_title=tournament_title,
                              host=tournament_host,
                              entrants=tournament_entrants,
                              bracket_type=tournament_bracket_type,
                              game_type=tournament_game_type,
                              date=tournament_date,
                              name=tournament_name)

  db.session.add(new_tournament)
  db.session.commit()
  print new_tournament
  return new_tournament
