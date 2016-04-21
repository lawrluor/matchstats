#!flask/bin/python

from app import app, db
from app.models import *
from trueskill_functions import *
import time

# Script run from shell calling ./recalculate_trueskill.py 
def main():
  start = time.time()

  recalculate_trueskill()
  
  end = time.time()
  elapsed = end - start
  print "Total time:", elapsed

if __name__ == "__main__":
  main()
