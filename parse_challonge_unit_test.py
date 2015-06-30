#!flask/bin/python
#Currently using fake setlist item

import os
import unittest

from config import basedir
from app import app, db
from app.models import *
from h2h_stats_functions import *

setlist = [[{'score': '1', 'tag': 'P4K EMP Armada', 'seed': '1', 'round': '1'}, {'score': '0', 'tag': 'GK Pi', 'seed': '2', 'round': '1'}], 
[{'score': '1', 'tag': 'CTRL DJ Nintendo', 'seed': '3', 'round': '1'}, {'score': '0', 'tag': 'GameGuys Mojo', 'seed': '4', 'round': '1'}], 
[{'score': '1', 'tag': 'Fiction', 'seed': '5', 'round': '1'}, {'score': '0', 'tag': 'Jake13', 'seed': '6', 'round': '1'}], 
[{'score': '1', 'tag': 'Crs.Chillindude', 'seed': '7', 'round': '1'}, {'score': '0', 'tag': 'GK Gahtzu', 'seed': '8', 'round': '1'}], 
[{'score': '1', 'tag': 'Crs.Hungrybox', 'seed': '9', 'round': '1'}, {'score': '0', 'tag': 'Zidane', 'seed': '10', 'round': '1'}], 
[{'score': '1', 'tag': 'Liquid`KDJ', 'seed': '11', 'round': '1'}, {'score': '0', 'tag': 'CTRL The Moon', 'seed': '12', 'round': '1'}]]

print "Testing selections from setlist"
print "setlist[1] should be DJ Nintendo vs Mojo"
print setlist[1]
print '\n'
print "setlist[1][0] should be DJ Nintendo's top half entry"
print setlist[1][0]
print '\n'
print "setlist[1][0]['tag'] should be the tag CTRL DJ Nintendo"
print setlist[1][0]['tag']
print '\n'