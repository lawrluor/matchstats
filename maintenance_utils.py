from app import app, db
from app.models import *

import sys
sys.path.append('./sanitize')
from sanitize_utils import check_and_sanitize_tag

from trueskill import setup, Rating, quality_1vs1, rate_1vs1
from trueskill_functions import MU, SIGMA, BETA, TAU, DRAW_PROBABILITY, populate_trueskills

  # Changes User's tag, given string new_tag. Also ensures that user's tag is changed in the Sets he has played
def change_tag(tag, new_tag):
  user = User.query.filter(User.tag==tag).first()
  print "ORIGINAL USER: ", user 
  
  won_sets = user.get_won_sets()
  for set in won_sets:
    set.winner_tag = new_tag
    print set
  
  lost_sets = user.get_lost_sets()
  for set in lost_sets:
    set.loser_tag = new_tag
    print set
  
  user.tag = new_tag
  db.session.commit()
  print "UPDATED USER: ", user
  print user.get_all_sets()

# Given a User tag and region name, changes user.region and changes regional trueskill if region is valid, otherwise deletes it
def change_region(tag, region_name):
  user = User.query.filter(User.tag==tag).first()
  region = Region.query.filter(Region.region==region_name).first()

  if user.region is not None and user.region.region==region_name:
    return "Region %s is already region of %s" % (region_name, tag)
  user.region = region
  
  # Repopulate regional trueskill for new region, to the default. First call deletes obsolete region, second call repopulates regional trueskill with new region. 
  # If new region is None, deletes obsolete region and does nothing else
  # If user.region was already None, does nothing
  populate_trueskills(user)
  populate_trueskills(user)
  db.session.commit()
  return user

def add_characters(tag, main, secondaries):
  found_tag = check_and_sanitize_tag(tag)
  if found_tag is None:
    found_tag = tag
  print found_tag

  user = User.query.filter(User.tag==found_tag).first()
  print user
  if user is None:
    return "User not found"

  user.main = main
  if secondaries is not None and secondaries!=[]:
    for secondary in secondaries:
      user.add_secondary(secondary)

  db.session.commit()
  return user


