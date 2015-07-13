#!flask/bin/python
# Manually enter dates for Challonge tournaments

from config import basedir
from app import app, db
from app.models import *
import datetime

# Query database
tournamentlist = Tournament.query.all()

# Assign variable for each Tournament object
BEAST_5 = tournamentlist[0]
PARAGON_ORLANDO_2015 = tournamentlist[1]
APEX_2015 = tournamentlist[2]
INY = tournamentlist[3]
MVG_SANDSTORM = tournamentlist[4]
PRESS_START = tournamentlist[5]
BAM_7 = tournamentlist[6]
GOML_2015 = tournamentlist[7]
CEO_2015 = tournamentlist[8]
FC_SMASH = tournamentlist[9]
WTFOX = tournamentlist[10]

# Manual Date Entry
PARAGON_ORLANDO_2015.date = datetime.date(2015, 1, 18)
APEX_2015.date = datetime.date(2015, 2, 1)
INY.date = datetime.date(2015, 4, 11)
MVG_SANDSTORM.date = datetime.date(2015, 4, 19)
PRESS_START.date = datetime.date(2015, 5, 10)
BAM_7.date = datetime.date(2015, 5, 24)
GOML_2015.date = datetime.date(2015, 5, 31)
FC_SMASH.date = datetime.date(2015, 7, 5)
WTFOX.date = datetime.date(2015, 7, 11)

print PARAGON_ORLANDO_2015.date
print APEX_2015.date
print INY.date
print MVG_SANDSTORM.date
print PRESS_START.date
print BAM_7.date
print GOML_2015.date
print FC_SMASH.date
print WTFOX.date
print '\n'

# Manual Entrants Entry
BAM_7.entrants = 32

print BAM_7.entrants

db.session.commit()
