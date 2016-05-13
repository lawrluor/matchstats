#!flask/bin/python

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
