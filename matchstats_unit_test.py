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

print "Testing User connections to Set"
Shroomed = userlist[0]
Hungrybox = userlist[1]
KirbyKaze = userlist[2]
aMSa = userlist[3]
PPMD = userlist[4]
Armada = userlist[5]
Leffen = userlist[6]
Mango = userlist[7]
Tonic = userlist[8]
Wyne = userlist[9]
print '\n'

print "Testing User.getWonSets"
shroomed_won_sets = Shroomed.getWonSets()
print shroomed_won_sets
hungrybox_won_sets = Hungrybox.getWonSets()
print hungrybox_won_sets
print '\n'


print "Testing User.getLostSets"
kirbykaze_lost_sets = KirbyKaze.getLostSets()
print kirbykaze_lost_sets
aMSa_lost_sets = aMSa.getLostSets()
print aMSa_lost_sets
print '\n'

print "Testing User.getAllSets()"
PPMD_all_sets = PPMD.getAllSets()
print PPMD_all_sets
Leffen_all_sets = Leffen.getAllSets()
print Leffen_all_sets
print '\n'

print "Testing Set connections to User"
hungrybox_shroomed = setlist[0]
aMSa_kirbykaze = setlist[1]
leffen_mango = setlist[2]
PPMD_armada = setlist[3]
mango_aMSa = setlist[4]
armada_hungrybox = setlist[5]
armada_mango = setlist[6]
PPMD_leffen = setlist[7]
armada_leffen = setlist[8]
armada_PPMD_GF1 = setlist[9]
PPMD_armada_GF2 = setlist[10]
wyne_tonic = setlist[11]
print '\n'

print "Testing Set.getSetWinner()"
print hungrybox_shroomed.getSetWinner()
print aMSa_kirbykaze.getSetWinner()
print '\n'

print "Testing Set.getSetWinnerID()"
print hungrybox_shroomed.getSetWinnerID()
print aMSa_kirbykaze.getSetWinnerID()
print '\n'

print "Testing Set.getSetLoser()"
print leffen_mango.getSetLoser()
print PPMD_armada.getSetLoser()
print '\n'

print "Testing Set.getSetLoserID"
print leffen_mango.getSetLoserID()
print PPMD_armada.getSetLoserID()
print '\n'


#clear non APEX 2015 users, sets, and matches
for user in userlist[8:]:
	db.session.delete(user)

for set in setlist[11:]:
	db.session.delete(set)

print userlist
print setlist

db.session.commit()

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