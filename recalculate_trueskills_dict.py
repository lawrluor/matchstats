#!flask/bin/python

from app import app, db
from app.models import *
from trueskill_functions import *
import time

# Script run from shell calling ./recalculate_trueskill.py 
def main():
  start = time.time()
  
  reset_all_trueskills()
  recalculate_trueskills_dict()
  recalculate_ranks("Global")
  recalculate_ranks("New England")
  recalculate_ranks("SoCal")

  end = time.time()
  elapsed = end - start
  print "Total time:", elapsed

if __name__ == "__main__":
  main()
