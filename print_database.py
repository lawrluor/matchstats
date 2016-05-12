#!flask/bin/python

# Prints entire database

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
characterlist = Character.query.all()

# Print current database
print "USERS:", User.query.all()
print "SETS:", Set.query.all()
print "MATCHES:", Match.query.all()
print "TOURNAMENTS:", Tournament.query.all()
print "REGIONS:", Region.query.all()
print "CHARACTERS:", Character.query.all()
