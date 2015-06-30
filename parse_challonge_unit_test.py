#!flask/bin/python

from app import app, db
from app.models import *

import urllib3
from bs4 import BeautifulSoup
import re

from parse_challonge import *

# Simulation of what would happen if one called these methods from parse_challonge from anywhere
matchlist = parse_challonge("http://ceogaming.challonge.com/ceo2014ssbmtop32")
import_challonge_data(matchlist, "CEO 2014")

print "Printing Userlist and Setlist"
userlist = User.query.all()
for user in userlist:
	print user
print '\n'

setlist = Set.query.all()
for set in setlist:
	print set
print '\n'