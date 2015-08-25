#!flask/bin/python

from app import app, db
from app.models import *
from trueskill_functions import *

# Script run from shell calling ./recalculate_trueskill.py 
def main():
  recalculate_trueskill()
  
if __name__ == "__main__":
  main()
