#!flask/bin/python

import sys
from parse_challonge.parse_challonge_standings import *
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

      parse_challonge_run(tournament_url, tournament_name)
 
  f.close()

if __name__ == "__main__":
  main()
