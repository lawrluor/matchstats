#!flask/bin/python

from app import app, db
from app.models import *
from trueskill_functions import *

def main():
  # Reset all User Trueskill to defaults
  userlist = User.query.all()
  for user in userlist:
    reset_trueskill(user)

  # Iterate through all Sets in order and recalculate Trueskill; currently in order of set.id
  setlist = Set.query.all()
  for set in setlist:
    winner_user = User.query.filter(User.tag==set.winner_tag).first()
    loser_user = User.query.filter(User.tag==set.loser_tag).first()
    update_rating(winner_user, loser_user)

  print "All trueskills recalculated"
  
if __name__ == "__main__":
  main()
