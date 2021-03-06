#!flask/bin/python

# Clears entire database except for Regions, Characters
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from config import basedir
from app import app, db
from app.models import *

# Query database
userlist = User.query.all()
setlist = Set.query.all()
matchlist = Match.query.all()
headerlist = TournamentHeader.query.all()
tournamentlist = Tournament.query.all()
regionlist = Region.query.all()

for user in userlist:
	db.session.delete(user)

for set in setlist:
	db.session.delete(set)

for match in matchlist:
	db.session.delete(match)

for header in headerlist:
	db.session.delete(header)

# Keep default "Non-Tourney" Tournament object at id=1, index=0
for i in range(len(tournamentlist)):
	db.session.delete(tournamentlist[i])

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
