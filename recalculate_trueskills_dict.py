#!flask/bin/python

from app import app, db
from app.models import *
from trueskill_functions import *
import time

# Script run from shell calling ./recalculate_trueskill.py 
def main():
  start = time.time()
  
  print "Resetting Trueskills"
  reset_all_trueskills()

  print "Recalculating Trueskills"
  recalculate_trueskills_dict()

  print "Recalculating Ranks"
  recalculate_ranks("Global")
  recalculate_ranks("New England")
  recalculate_ranks("SoCal")

  end = time.time()
  elapsed = end - start
  print "Total time:", elapsed

if __name__ == "__main__":
  main()
