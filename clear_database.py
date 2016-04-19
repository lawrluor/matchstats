#!flask/bin/python

# Clears entire database except for Regions, Characters

import os
import unittest

from config import basedir
from app import app, db
from app.models import *

# Query database
userlist = User.query.all()
setlist = Set.query.all()
matchlist = Match.query.all()
tournamentlist = Tournament.query.all()
regionlist = Region.query.all()
subtournamentlist = SubTournament.query.all()

for user in userlist:
	db.session.delete(user)

for set in setlist:
	db.session.delete(set)

for match in matchlist:
	db.session.delete(match)

# Keep default "Non-Tourney" Tournament object at id=1, index=0
for i in range(len(tournamentlist)):
	db.session.delete(tournamentlist[i])

for sub_tournament in subtournamentlist:
	db.session.delete(sub_tournament)

# Keep regions
# for i in range(len(regionlist)):
# 	db.session.delete(regionlist[i])

# create default "Non-Tourney" Tournament object at id=1
# non_tourney = Tournament(id=1, name="Non-Tourney")
# db.session.add(non_tourney)

db.session.commit()

# Print newly cleared database
print "USERS:", User.query.all()
print "SETS:", Set.query.all()
print "MATCHES:", Match.query.all()
print "TOURNAMENTS:", Tournament.query.all()
print "REGIONS:", Region.query.all()
