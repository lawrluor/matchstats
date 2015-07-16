#!flask/bin/python

# Unit Test for head to head functions. Earlier h2h function tests are in matchstats_unit_test.py

import os
import unittest

from config import basedir
from app import app, db
from app.models import *
from h2h_stats_functions import *

print "Leffen and Mew2King h2h_get_mutual_tournaments"
h2h_get_mutual_tournaments("Leffen", "Mew2King")
print '\n'

print "Armada and Leffen h2h_get_mutual_tournaments"
h2h_get_mutual_tournaments("Armada", "Leffen")
print '\n'