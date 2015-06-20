#!flask/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Set, Match

userlist = User.query.all()
setlist = Set.query.all()
matchlist = Match.query.all()

print userlist
print '\n'
print setlist
print '\n'
print matchlist

print "Testing User and Set connections"
Tonic = userlist[0]
print '\n'

print "Testing User.getWonSets"
Tonic_won_sets = User.getWonSets(Tonic)
print Tonic_won_sets
print '\n'

print "Testing User.getLostSets"
Tonic_lost_sets = User.getLostSets(Tonic)
print Tonic_lost_sets
print '\n'

print "Testing User.getAllSets"
Tonic_all_sets = User.getAllSets(Tonic)
print Tonic_all_sets
print '\n'

"""
#clear database
for user in userlist:
	db.session.delete(user)

for set in setlist:
	db.session.delete(set)

for match in matchlist:
	db.session.delete(match)

print userlist
print setlist
print matchlist

db.session.commit()
"""