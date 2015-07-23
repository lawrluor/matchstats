#!flask/bin/python
# Clears entire non-Character database

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

for user in userlist:
	db.session.delete(user)

for set in setlist:
	db.session.delete(set)

for match in matchlist:
	db.session.delete(match)

# Keep default "Non-Tourney" Tournament object at id=1, index=0
for i in range(len(tournamentlist)):
	db.session.delete(tournamentlist[i])

"""
for i in range(len(regionlist)):
	db.session.delete(regionlist[i])
"""


"""
# create default "Non-Tourney" Tournament object at id=1
non_tourney = Tournament(id=1, name="Non-Tourney")
db.session.add(non_tourney)
"""

db.session.commit()

print userlist
print setlist
print matchlist
print tournamentlist
print regionlist
