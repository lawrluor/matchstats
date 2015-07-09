#!flask/bin/python
# Prints entire non-Character database

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

print userlist
print setlist
print matchlist
print tournamentlist
