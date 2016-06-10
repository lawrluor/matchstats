#!flask/bin/python

# Like character_create.py, creates a static list of Region objects that will be active in the database.

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from config import basedir
from app import app, db
from app.models import *

print "Print current Region database"
regionlist = Region.query.all()
print regionlist
print '\n'

# Create all additional regions
New_England = Region(region="New England")
NorCal = Region(region="NorCal")
SoCal = Region(region="SoCal")
North_Carolina = Region(region="North Carolina")

# Add and commit to database
db.session.add(New_England)
db.session.add(NorCal)
db.session.add(SoCal)
db.session.add(North_Carolina)

db.session.commit()

print "Print new Region database"
regionlist = Region.query.all()
print regionlist

# Region query commands
# ne_users = User.query.join(Region, User.region).filter(Region.region=="New England").all()
# ne_tournaments = Tournament.query.join(Region, Tournament.region).filter(Region.region=="New England").all()
