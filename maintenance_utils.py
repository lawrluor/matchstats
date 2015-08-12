from app import app, db
from app.models import *
import datetime

import sys
sys.path.append('./sanitize')
from sanitize_utils import check_and_sanitize_tag

from trueskill import setup, Rating, quality_1vs1, rate_1vs1
from trueskill_functions import MU, SIGMA, CONS_MU, BETA, TAU, DRAW_PROBABILITY, populate_trueskills

# Changes User's tag, given string new_tag. Also ensures that user's tag is changed in the Sets he has played
def change_tag(tag, new_tag):
  user = User.query.filter(User.tag==tag).first()
  if user is None:
    print "User %s not found." % tag
    return
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
  return user

# transfers the data the User represented by joined_tag has to User root_tag, while deleting the User represented by joined_tag
# currently doesn't actually link the Users or tag in any way before deletion
# currently doesn't change Matches
def merge_user(root_tag, joined_tag):
  root_user = User.query.filter(User.tag==root_tag).first()
  joined_user = User.query.filter(User.tag==joined_tag).first()
  if root_user is None: 
    print "root_user not found"
    return
  elif joined_user is None: 
    print "joined_user not found"
    return

  # transfer Set data by simply editing Sets to have the root_user as the winner/loser tag and id
  joined_sets = joined_user.get_all_sets()
  for set in joined_sets:
    if set.winner_tag==joined_user.tag:
      set.winner_tag = root_user.tag
      set.winner_id = root_user.id
    else:
      set.loser_tag = root_user.tag
      set.loser_id = root_user.id

  # merge Placement in joined_user by setting Placement.user = root_user
  # Placement object removed (from beginning of list, index 0) from joined_user.tournament_assocs upon changing identity of Placement.user, so start again from index 0
  while len(joined_user.tournament_assocs) > 0:
    joined_user.tournament_assocs[0].user = root_user

  db.session.delete(joined_user) 
  db.session.commit()
  return root_user

def search_and_replace_user(tag_string):
  userlist = User.query.filter(User.tag.contains(tag_string)).all()
  for user in userlist:
    print "USER TAG", user.tag
    new_tag = user.tag.replace(tag_string, '')
    print "NEW_TAG", new_tag
    sanitized_tag = check_and_sanitize_tag(new_tag, user.region)
    print "SANITIZED TAG", sanitized_tag

    # Find User if tag not registered
    if sanitized_tag is None:
      root_user = User.query.filter(User.tag==new_tag).first()
      if root_user is not None:
        print "ROOT USER", root_user
        merge_user(root_user.tag, user.tag)
      else:
        # if still can't find root tag to merge with, then root tag doesn't exist. Change the tag
        change_tag(user.tag, new_tag)
    else:
      # if found sanitized User, merge them
      merge_user(sanitized_tag, user.tag)  
    print '\n'

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

  db.session.commit()
  return user

# Given parameter tournament name and a list of integers representing year, month, and day, queries for Tournament object and assigns a date for it.
def change_date(tournament_name, date_numbers):
  tournament = Tournament.query.filter(Tournament.name==tournament_name).first()
  if tournament is None:
    return "Tournament not found"

  # Create date object, index 0 = year, index 1 = month, index 2 = day
  date = datetime.date(date_numbers[0], date_numbers[1], date_numbers[2])
  tournament.date = date
  
  db.session.commit()
  return tournament
  
