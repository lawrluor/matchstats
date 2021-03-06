#!flask/bin/python
from app.models import *
import sys

import urllib3
from bs4 import BeautifulSoup
import re
import datetime
from datetime import date

"""
  This module contains utility functions for parsing challonge brackets.
"""
  

def parse_challonge_info(tournament_url):
  """Takes in a tournament url and outputs a dictionary with tournament
  information.

  If tournament_url is None, it returns None.

  Args:
      tournament_url: A string containing the challonge bracket url.

  Returns:
      A dict mapping tournament attributes to tournament values.
      'title': string : name of tournament.
      'host': string : challonge account that hosted the tournament.
      'game_type': string : game tournament plays (melee, brawl).
      'date': string : when the tournament was held.
      'entrants': int : number of entrants.
      'bracket_type': string : bracket information (ex. 64-player double elimination).
  """
  if tournament_url is None: return None
  conn3 = urllib3.connection_from_url(tournament_url)
  r3 = conn3.request("GET", tournament_url)
  soup3 = BeautifulSoup(r3.data)
  soup3.prettify()

  tournament_info = {}

  title_item = soup3.find("div", id='title') 
  if title_item is not None:
    title = title_item.getText()
    title = title.strip('\n')
    # protect from overflowing database column, truncate at 128 characters
    title = title[:128]
    tournament_info['title'] = title
    print "TITLE:", title

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
    # protect from overflowing database column, truncate at 128 characters
    host = host[:128]
    tournament_info['host'] = host
    print "HOST:", host

  game_type_item = soup3.find("a", {"href" : re.compile('http://challonge.com/games/.*')})
  if game_type_item is not None:
    game_type = game_type_item.getText()
    game_type = game_type.strip('\n')
    game_type = game_type[:128]
    tournament_info['game_type'] = game_type
    print "GAME_TYPE:", game_type

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
    print "DATE:", date
  
  # locates an info icon near the bracket type description, because the bracket_type description does not exist inside a tag
  bracket_locator = soup3.find("i", {"class" : "icon-info-sign"})
  if bracket_locator is not None:
    # next line happens to contain a string with the bracket information and entrant number, i.e. "32 player Double Elimination", or a two-stage bracket info, i.e. "Groups (16 &rarr; 2) then Double Elimination"
    type_index = bracket_locator.nextSibling.find("then")
    if type_index == -1:
      bracket_info = bracket_locator.nextSibling
    else:
      bracket_info = bracket_locator.nextSibling[(type_index + 5):]

    # protect from overflowing database column, truncate at 128 characters
    bracket_info = bracket_info[:128]
    print "BRACKET INFO:", bracket_info

    # find start index for player, subtract 1 (whitespace) to get just the number of entrants "32" and convert to int
    player_index = bracket_info.find("player") 
    if player_index != -1:
      entrants = int(bracket_info[:(player_index-1)])
      # use index when "player" starts, player_index, and account for the word and whitespace to get everything after "player "
      bracket_type = bracket_info[(player_index+7):].strip('\n')
    else:
      entrants = -1 
      bracket_type = bracket_info.strip('\n')

    tournament_info['entrants'] = entrants
    bracket_type = bracket_type[:128]
    tournament_info['bracket_type'] = bracket_type
    print "ENTRANTS:", entrants
    print "BRACKET TYPE:", bracket_type
  print "OVERALL TOURNAMENT INFO:", tournament_info
  return tournament_info

# Given processed tournament_info dict from parse_tournament_info or parse_challonge_info, add Tournament object to database with the appropriate information
# get tourney title, host, number of entrants, bracket type, game type, and date given an info dictionary from parse_challonge_info, and a string tournament_name, and create and return a Tournament object
def import_challonge_info(tournament_info, tournament_name, tournament_region, tournament_date):
  if 'title' in tournament_info:
    tournament_title = tournament_info['title']
  else:
    tournament_title = None
  
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
    tournament_game_type = "Super Smash Bros. Melee"

  # if date located in Challonge bracket, use this date, otherwise use date passed in as parameter
  if 'date' in tournament_info:
    print tournament_info['date']
    tournament_date = convert_date(tournament_info['date'])
  else:
    if tournament_date is not None:
      tournament_date = tournament_date
    else:
      tournament_date = datetime.date(2099, 01, 01)
  print "DATE", tournament_date

  if 'url' in tournament_info:
      tournament_url = tournament_info['url']
  else:
      tournament_url = None

  if tournament_name is None:
    tournament_name = "Non-Tourney"
 
  print "REGION", tournament_region

  new_tournament = Tournament(official_title=tournament_title,
                              host=tournament_host,
                              url=tournament_url,
                              entrants=tournament_entrants,
                              bracket_type=tournament_bracket_type,
                              game_type=tournament_game_type,
                              date=tournament_date,
                              name=tournament_name)

  db.session.add(new_tournament)

  # add tournament_region; if None, then it adds None
  found_region = Region.query.filter(Region.region==tournament_region).first()
  new_tournament.region = found_region

  db.session.commit()
  return new_tournament

# static dictionary to convert calendar date to datetime, used in convert_date
months = {'January' : 1,
          'February' : 2,
          'March' : 3,
          'April' : 4,
          'May' : 5,
          'June' : 6,
          'July' : 7, 
          'August' : 8, 
          'September' : 9,
          'October' : 10,
          'November' : 11,
          'December' : 12}

# Converts a date styled June 28, 2015 into datetime 2015-06-28
def convert_date(challonge_date):
  date_parser = re.compile('[/ ,-]+') 
  tokens = date_parser.split(challonge_date)
  # print tokens
  
  # integer representing month
  month = months[tokens[0]]
  day = int(tokens[1])
  year = int(tokens[2])
  # print month, day, year

  date = datetime.date(year=year, month=month, day=day)
  # print date
  return date

# Converts a date styled 06-28-2015 into datetime 2015-06-28
def convert_int_date(int_date):
  date_parser = re.compile('[/ ,-]+') 
  tokens = date_parser.split(int_date)
  # print tokens
  
  # integer representing month
  month = int(tokens[0])
  day = int(tokens[1])
  year = int(tokens[2])
  # print month, day, year

  date = datetime.date(year=year, month=month, day=day)
  # print date
  return date
