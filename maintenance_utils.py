from app import app, db
from app.models import *
import datetime

import sys
sys.path.append('./sanitize')
from sanitize_utils import *

from trueskill import setup, Rating, quality_1vs1, rate_1vs1
from trueskill_functions import MU, SIGMA, CONS_MU, BETA, TAU, DRAW_PROBABILITY, populate_trueskills
from misc_utils import *
# Make some of these Class functions in app.models??

# Changes User's tag, given string new_tag. Also ensures that user's tag is changed in the Sets he has played
def change_tag(tag, new_tag):
  user = User.query.filter(User.tag==tag).first()
  if user is None:
    print "User %s not found." % tag
    return
  print "ORIGINAL USER: ", print_ignore(user)

  won_sets = user.get_won_sets()
  for set in won_sets:
    set.winner_tag = new_tag
    print_ignore(set)
  
  lost_sets = user.get_lost_sets()
  for set in lost_sets:
    set.loser_tag = new_tag
    print_ignore(set)

  user.tag = new_tag
  
  db.session.commit()
  print "UPDATED USER: ", print_ignore(user)
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
  placements = joined_user.tournament_assocs
  compare_from = 0
  while len(placements) > compare_from:
    # Screen for case in which both joined_user and root_user present in same tourney
    # Example: http://bigbluees.challonge.com/NGP44, joined_user="elicik", root_user="Elicik"
    duplicates = Placement.query.filter(and_(Placement.user_id==root_user.id, Placement.tournament_id==placements[compare_from].tournament_id)).all()
    print duplicates, len(duplicates), compare_from
    if len(duplicates)>0:
      # if 1 or more duplicates, keep placement, and begin comparing from the next index
      compare_from += 1

    # Prevent index out of bound error if len(placements)=0; if User only entered one tournament
    if len(placements)>compare_from:
      print placements[compare_from]
      placements[compare_from].user = root_user
    else:
      print placements[compare_from-1]
      placements[compare_from-1].user = root_user
    print root_user.tournament_assocs[-1]
    print '\n'

  # If there were duplicates, don't delete the joined_user as it is a legit other User who happens to have the same tag after conversion.
  if compare_from==0:
    db.session.delete(joined_user)
    db.session.commit()
    return root_user
  else:
    print "DUPLICATE WAS FOUND"
    return root_user

def capitalize_all_tags():
  # Not used in sanitize because if people come with sponsor tags, they will be deleted anyways and real tag won't be the same
  userlist = User.query.all()
  for user in userlist:
    if not user.tag[0].isalpha() or user.tag[0].isupper():
      continue
    else:
      print "USER TAG", print_ignore(user.tag)
      temp = user.tag
      capitalize_first = lambda s: s[:1].upper() + s[1:] if s else ''
      cap_tag = capitalize_first(temp)
      print "CAP TAG", print_ignore(cap_tag)

    root_user = User.query.filter(User.tag==cap_tag).first()
    if root_user is not None:
      print "ORIGINAL USER", print_ignore(user)
      print "ROOT USER", print_ignore(root_user)
      merge_user(root_user.tag, user.tag)
    else:
      # if can't find root tag to merge with, then root tag doesn't exist. Change the tag
      change_tag(user.tag, cap_tag)
    print '\n'
  return

def remove_team(separator):
  userlist = User.query.filter(User.tag.contains(separator)).all()
  for user in userlist:
    print "USER TAG", user.tag
    sep_index = user.tag.rfind(separator)
    # ensure you are removing from the front. checks against cases where separator is last char
    if sep_index!=len(user.tag)-1:
      new_tag = user.tag[sep_index+len(separator):]
      new_tag = new_tag.strip()
      print "NEW TAG", new_tag
    else:
      print "Not a team separator"
      continue

    if user.region is None:
      sanitized_tag = check_and_sanitize_tag(new_tag)
    else:
      sanitized_tag = check_and_sanitize_tag(new_tag, user.region.region)
    print "SANITIZED TAG", sanitized_tag

    # Find User if tag not registered
    if sanitized_tag==new_tag:
      # this means user was not matched to sanitized tag, so query for user with tag==new_tag
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


def search_and_replace_user(tag_string):
  userlist = User.query.filter(User.tag.contains(tag_string)).all()
  for user in userlist:
    print "USER TAG", user.tag
    new_tag = user.tag.replace(tag_string, '')
    new_tag = new_tag.strip()
    print "NEW_TAG", new_tag

    if user.region is None:
      sanitized_tag = check_and_sanitize_tag(new_tag)
    else:
      sanitized_tag = check_and_sanitize_tag(new_tag, user.region.region)
    print "SANITIZED TAG", sanitized_tag

    # Find User if tag not registered
    if sanitized_tag==new_tag:
      # this means user was not matched to sanitized tag, so query for user with tag==new_tag
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

def add_characters(tag, characters):
  found_tag = check_and_sanitize_tag(tag)
  print found_tag

  user = User.query.filter(User.tag==found_tag).first()
  print user
  if user is None:
    return "User not found"

  if characters is not None and characters !=[]:
    for character in characters:
      user.add_character(character)
      db.session.commit()
  db.session.commit()
  return user

def delete_character(tag, character):
  user = User.query.filter(User.tag==tag).first()
  user.remove_character(character)
  db.session.commit()

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

# given Tournament object, if tournament name already exists, if tournament is a pool of a larger one, add placements and sets to Tournament object and return it, else simply return original Tournament object
def check_tournament(tournament):
  same_tournament = Tournament.query.filter(Tournament.name==tournament.name).first()
  # if tournament already exists, only add matches to Tournament, else create tournament as usual
  if same_tournament is not None:
    # if tournament.type == "Pool"
    same_tournament.sets.append(tournament.sets) 
  else:
    print "Tournament already exists" 
  return same_tournament

# given user tag, returns a simple dictionary with keys tournament_name and value placement for a tournament a User has attended
def get_tournament_name_and_placing(user_tag):
  user = User.query.filter(User.tag==user_tag).first()
  user_placements = {}

  for tournament_placement in user.tournament_assocs:
    tournament_name = tournament_placement.tournament.name
    placement  = convert_placement(tournament_placement.placement)
    user_placements[tournament_name] = placement

  print user_placements
  return user_placements

# deletes a Set given tournament name, set winner, and set loser 
def delete_set(tournament_name, winner_tag, loser_tag):
  winner_user = User.query.filter(User.tag==winner_tag).first()
  loser_user = User.query.filter(User.tag==loser_tag).first()
  if winner_user is None: 
    print "winner_user not found"
    return
  elif loser_user is None: 
    print "loser_user not found"
    return

  found_set = Set.query.filter(and_(Set.loser_tag==loser_tag, Set.winner_tag==winner_tag, Set.tournament_name==tournament_name)).all()
  if len(found_set)==1:
    db.session.delete(found_set[0])
    db.session.commit()
    print "Set deleted"
    return
  elif len(found_set) < 1:
    return "No set found"
  elif len(found_set) > 1:
    return "Multiple Sets found"

# reassigns Tournament Placement and Sets from one User to another
def reassign_user(tournament_name, user_tag, reassigned_tag):
  # Query for objects
  found_user = User.query.filter(User.tag==user_tag).first()
  reassigned_user = User.query.filter(User.tag==reassigned_tag).first() 

  # find placement User has in Tournament, and replace found_user with reassigned_user
  found_placement = Placement.query.filter(and_(Placement.tournament_name==tournament_name, Placement.user==found_user)).first()
  if found_placement is not None:
    found_placement.user=reassigned_user
  else:
    print "Placement not found"
  
  # find Sets User played in Tournament, and replace the found_user with reassigned_user
  found_sets = Set.query.filter(and_(Set.tournament_name==tournament_name), or_(Set.winner_tag==user_tag, Set.loser_tag==user_tag)).all()
  print found_sets
  if found_sets is not None:
    for found_set in found_sets:
      if found_set.winner_tag==user_tag:
        found_set.winner_tag=reassigned_tag
      elif found_set.loser_tag==user_tag:
        found_set.loser_tag=reassigned_tag
  else:
    print "No Sets found"

  db.session.commit()
  return "Tournament entries reassigned" 
