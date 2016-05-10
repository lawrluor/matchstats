#!flask/bin/python

import re
import sys
from process_tournament import *

def main():
  '''
  Takes args from command prompt:
  tournamentlist is a .txt file from tournamentlists subfolder
  region is a string that is the name of an existing Region
  Example call: ./process_tournamentlist.py tournamentlists/modern_NE_tournamentlist.txt "New England"
  '''
  tournamentlist = sys.argv[1]
  region = sys.argv[2]
  read_tournamentlist(tournamentlist, region)

def read_tournamentlist(tournamentlist, region):
  # f is a file object
  with open(tournamentlist, 'r') as f:
    for tournament_line in f:
      process_tournament_line(tournament_line, region)
  f.close()

if __name__ == "__main__":
  main()


