#!flask/bin/python

import sys
sys.path.append('./parse_challonge')
from parse_challonge_standings import *
from parse_challonge_info import *
from parse_challonge_matches import *
from parse_challonge_run import *

import re


def main():
  challonge_tournamentlist = sys.argv[1]
  read_tournamentlist(challonge_tournamentlist)

def read_tournamentlist(challonge_tournamentlist):
  # f is a file object
  with open(challonge_tournamentlist, 'r') as f:
    for tournament_line in f:
      # process each line and parse tournament_url, tournament_name 
      processed_tournament_line = tournament_line.strip('\n')
      line_parser = re.compile('[|]')
      tokens = line_parser.split(processed_tournament_line)
      tournament_name = tokens[0]
      # Remove '\' escape characters
      tournament_name = tournament_name.translate(None, '\\')
      tournament_url = tokens[1]
      tournament_region = tokens[2]
      
      # If region passed as string "None", convert to None object
      if tournament_region=="None":
        tournament_region = None

      tournament_region = tournament_region.translate(None, '\\')
      print tournament_name + ': ' + tournament_url
 
      # process 4th parameter, tournament_date, and convert  to datetime object
      tournament_date = tokens[3]
      tournament_date = convert_int_date(tournament_date)

      parse_challonge_run(tournament_url, tournament_name, tournament_region, tournament_date)
  f.close()

if __name__ == "__main__":
  main()
