#! flask/bin/python

from app import app, db
from app.models import *
from trueskill_functions import *

print "test0.skill_assocs is empty, and region is None: should be populated with Global TrueSkill"
test0 = User(tag="test0")
populate_trueskills(test0)
print test0, test0.skill_assocs
print '\n'

print "testA.skill_assocs is empty, and region is populated: should be populated with Global and Region TrueSkill"
testA = User(tag="testA")
testA.region=Region.query.first()
populate_trueskills(testA)
print testA, testA.skill_assocs
print '\n'


print "test1.skill_assocs contains Global TrueSkill: should remain populated with Global TrueSkill"
test1 = User(tag="test1")
test1.skill_assocs.append(UserSkills(region="Global", trueskill=TrueSkill(mu=22, sigma=9)))
populate_trueskills(test1)
print test1, test1.skill_assocs
print '\n'

print "testB.skill_assocs contains Global TrueSkill, and region is populated: should add Region TrueSkill and remain populated with Global TrueSkill"
testB = User(tag="testB")
testB.region=Region.query.first()
testB.skill_assocs.append(UserSkills(region="Global", trueskill=TrueSkill(mu=22, sigma=9)))
populate_trueskills(testB)
print testB, testB.skill_assocs
print '\n'

print "test2.skill_assocs contains Global and Region TrueSkill and region is populated; should remain populated with both TrueSkills"
test2 = User(tag="test2")
test2.region=Region.query.first()
test2.skill_assocs.append(UserSkills(region="Global", trueskill=TrueSkill(mu=20, sigma=7)))
test2.skill_assocs.append(UserSkills(region=test2.region.region, trueskill=TrueSkill(mu=30, sigma=4)))
populate_trueskills(test2)
print test2, test2.skill_assocs
print '\n'

print "Testing update_rating"
print "test0 vs testA, Global ranking should update"
update_rating(test0, testA)
print '\n'

print "testA vs testB, Region ranking should update"
update_rating(testA, testB)
print '\n'

print "test1 vs testB, Global ranking should update"
update_rating(test1, testB)
print '\n'

print "test2 vs testB, Region ranking should update"
update_rating(test2, testB)
print '\n'

print "test2 vs testA, Region ranking should update"
update_rating(test2, testA)
print '\n'

print "test2 vs test0, Global ranking should update"
update_rating(test2, test0)
print '\n'


print "Testing reset_trueskill; all TrueSkill values should be default"
reset_trueskill(test0)
reset_trueskill(test1)
reset_trueskill(test2)
print test0, test0.skill_assocs
print test1, test1.skill_assocs
print test2, test2.skill_assocs

