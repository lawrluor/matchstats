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
      info = process_tournament_line(tournament_line)
      parse_challonge_run(info['tournament_url'], info['tournament_name'], info['tournament_region'], info['tournament_date'])
  f.close()

if __name__ == "__main__":
  main()


