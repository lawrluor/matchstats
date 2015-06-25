#!flask/bin/python

import os
import unittest
import sqlalchemy

from config import basedir
from app import app, db
from app.models import *


# Clean up database before use
userlist = User.query.all()
characterlist = Character.query.all()

for user in userlist[8:]:
	db.session.delete(user)

for character in characterlist:
	db.session.delete(character)

db.session.commit()


print "Testing User and Character Connection"
user1 = User(tag='MacD', region='Southern California', main='Peach')
character1 = Character(id=1, name='Fox')

db.session.add(user1)
db.session.add(character1)
db.session.commit()

print user1
print character1
print '\n'

# Tests start here
print "Testing User.is_linked; should return False"
print user1.is_linked(character1)
print '\n'

print "Testing User.link_secondaries"
print '\n'
user1.link_secondaries(character1)
db.session.commit()
print user1
print '\n'
print "Tests if User linked to character using User.is_linked: should now return True"
print user1.is_linked(character1)
print '\n'
print "Print all User's secondaries"
print user1.secondaries.all()
print '\n'

print "Testing User.get_secondaries"
print user1.get_secondaries(character1)
