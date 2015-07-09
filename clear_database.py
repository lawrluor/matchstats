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

for user in userlist:
	db.session.delete(user)

for set in setlist:
	db.session.delete(set)

for match in matchlist:
	db.session.delete(match)

# Keep default "Non-Tourney" Tournament object at id=1
for i in range(1, len(tournamentlist)):
	db.session.delete(tournamentlist[i])

db.session.commit()

print userlist
print setlist
print matchlist
print tournamentlist
