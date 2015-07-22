#!flask/bin/python

from config import basedir
from app import app, db
from app.models import *
from trueskill import setup, Rating, quality_1vs1, rate_1vs1
from trueskill_functions import *

# Set up Rating environment
rating_env_setup()

# Query database for userlist
userlist = User.query.all()
print userlist
user1 = userlist[0]
user2 = userlist[1]
print user1, user2

# Print initial trueskill values for User (User.trueskill)
print "Initial trueskill values for user1, user2"
print user1.trueskill, user2.trueskill

print "Testing trueskill ratings functionality and update_rating"
update_rating(user1, user2)

# Query Users and generate userlist ordered by Trueskill.mu (lowest to highest)
userlist =  User.query.join(TrueSkill, User.trueskill).order_by(TrueSkill.mu.desc()).all()
for user in userlist:
	print user