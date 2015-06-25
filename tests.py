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

print '\n'
print "Print all Users and Characters in current database"
userlist = User.query.all()
characterlist = Character.query.all()
print '\n'

print "Current userlist"
for user in userlist:
	print user
print '\n'

print "Current characterlist"
for character in characterlist:
	print character
print '\n'


# Tests start here
print "Testing User.is_secondary; should return False"
print user1.is_secondary(character1)
print user2.is_secondary(character2)
print '\n'

print "Testing User.add_secondaries"
user1.add_secondaries(character1)
db.session.commit()
print user1
print '\n'
user2.add_secondaries(character2)
db.session.commit()
print user2
print '\n'

print "Tests if Character now in User.secondaries using User.is_secondary: should now return True"
print user1.is_secondary(character1)
print user2.is_secondary(character2)
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
print "character1 not yet in User.secondaries, should return False"
print user2.is_secondary(character1)
user2.add_secondaries(character1)
print "character1 now in User.secondaries, is_secondary should now return True"
print user2.is_secondary(character1)
print user2
print '\n'

print "Testing User.remove_secondaries"
print "Removing character1 from user2"
user2.remove_secondaries(character1)
print user2
print user2.get_secondaries()
print '\n'
print "Removing character1 from user1"
user1.remove_secondaries(character1)
print user1
print "Removing character1 from user1: nothing should change"
user1.remove_secondaries(character1)
print user1
print '\n'
print "Removing character2 from user2"
user2.remove_secondaries(character2)
print user2
db.session.commit()
print '\n'

print "Add all characters back to users for further testing purposes"
user1.add_secondaries(character1)
user2.add_secondaries(character1)
user2.add_secondaries(character2)
db.session.commit()
print user1
print user2
print '\n'

"Testing Character-User functions from Character Class"
print "Print current characterlist"
print characterlist
print '\n'

print "Testing Character.get_users"
print "character1.get_users"
print character1.get_users()
print '\n'
print "character2.get_users"
print character2.get_users()
print '\n'

print "Testing Character.uses_secondary"
print "character1.uses_secondary(user1), should return True"
print character1.uses_secondary(user1)
print "character1.uses_secondary(user2), should return True"
print character1.uses_secondary(user2)
print '\n'
print "character2.uses_secondary(user1), should return False"
print character2.uses_secondary(user1)
print "character2.uses_secondary(user2), should return True"
print character2.uses_secondary(user2)
print '\n'


# Clear database to original form when finished
userlist = User.query.all()
characterlist = Character.query.all()

for user in userlist[8:]:
	db.session.delete(user)

for character in characterlist:
	db.session.delete(character)

db.session.commit()


