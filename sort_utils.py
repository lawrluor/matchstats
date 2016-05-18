from app import app, db
from app.models import *
from operator import attrgetter

# Given setlist, sorts first by tournament date backref, then by id so that the first set is the oldest one
def sort_setlist(setlist):
  sorted_setlist = sorted(setlist, key=attrgetter('tournament.date', 'id'))
  try:
  	return sorted_setlist
  except:
  	UnicodeEncodeError

# Given list of Placement objects, order by associated Tournament.date, then Tournament.name
def sort_placementlist(placementlist):
  sorted_placementlist = sorted(placementlist, key=attrgetter('tournament.date', 'tournament.name'), reverse=True)
  return sorted_placementlist

# CURRENTLY BROKEN
# Given list of User objects, order by trueskill.mu. Useful for sorting model backrefs to userlist (like region.users)
def sort_userlist(userlist):
  sorted_userlist = sorted(userlist, key=attrgetter('trueskill.mu'), reverse=True)


