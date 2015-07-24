#!flask/bin/python

# Like character_create.py, creates a static list of Region objects that will be active in the database.

from config import basedir
from app import app, db
from app.models import *

print "Print current Region database"
regionlist = Region.query.all()
print regionlist
print '\n'

# Create all additional regions
# Unknown_Region = Region(region="Unknown") # The default Region, rather than None.
New_England = Region(region="New England")

# Add and commit to database
# db.session.add(Unknown_Region)
db.session.add(New_England)

db.session.commit()

print "Print new Region database"
regionlist = Region.query.all()
print regionlist

# Region query commands
# ne_users = User.query.join(Region, User.region).filter(Region.region=="New England").all()
# ne_tournaments = Tournament.query.join(Region, Tournament.region).filter(Region.region=="New England").all()