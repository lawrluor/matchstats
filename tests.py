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

#Setup
print "Creating temporary Users and Characters"
user1 = User(tag='MacD', region='Southern California', main='Peach')
user2 = User(tag='Kira', region='Southern California', main='Sheik')
character1 = Character(id=1, name='Fox')
character2 = Character(id=3, name='Sheik')

db.session.add(user1)
db.session.add(character1)
db.session.add(user2)
db.session.add(character2)
db.session.commit()


print "Print all Users and Characters in current database"
userlist = User.query.all()
characterlist = Character.query.all()

for user in userlist:
	print user
print '\n'

for character in characterlist:
	print character
print '\n'


# Tests start here
print "Testing User.is_linked; should return False"
print user1.is_linked(character1)
print user2.is_linked(character2)
print '\n'

print "Testing User.link_secondaries"
user1.link_secondaries(character1)
db.session.commit()
print user1
print '\n'
user2.link_secondaries(character2)
db.session.commit()
print user2
print '\n'

print "Tests if User linked to character using User.is_linked: should now return True"
print user1.is_linked(character1)
print user2.is_linked(character2)
print '\n'
print "Print all User's secondaries"
print user1.secondaries.all()
print user2.secondaries.all()
print '\n'

print "Testing User.get_secondaries"
print "user1 Secondaries"
print user1.get_secondaries()
print '\n'
print "user2 Secondaries"
print user2.get_secondaries()
print '\n'

print "Appending Secondaries to Users"
print "user2 not yet linked with character1, should return False"
print user2.is_linked(character1)
user2.link_secondaries(character1)
print "user2 now linked with character1, is_linked should now return True"
print user2.is_linked(character1)
print user2.get_secondaries()
print user2
print '\n'
