#! flask/bin/python

from app import app, db
from app.models import *
from trueskill_functions import *

# tests for trueskill_functions

print "test0.trueskills is empty, and region is None: should be populated with Global TrueSkill"
# test0 = User(tag="test0")
test0 = check_set_user("test0")
populate_trueskills(test0)
print test0
print test0.tag, test0.trueskills
print test0.trueskills
print '\n'

print "testA.trueskills is empty, and region is populated: should be populated with Global and Region TrueSkill"
testA = check_set_user("testA")
testA.region=Region.query.first()
populate_trueskills(testA)
print testA
print testA.tag, testA.trueskills
print '\n'


print "test1.trueskills contains Global TrueSkill: should remain populated with Global TrueSkill"
test1 = check_set_user("test1")
test1.trueskills.append(TrueSkill(region="Global", mu=22, sigma=9, cons_mu=22-(9*3)))
populate_trueskills(test1)
print test1
print test1.tag, test1.trueskills
print '\n'

print "testB.trueskills contains Global TrueSkill, and region is populated: should add Region TrueSkill and remain populated with Global TrueSkill"
testB = check_set_user("testB")
testB.region=Region.query.first()
testB.trueskills.append(TrueSkill(region="Global", mu=22, sigma=9, cons_mu=22-(9*3)))
populate_trueskills(testB)
print testB
print testB.tag, testB.trueskills
print '\n'

print "test2.trueskills contains Global and Region TrueSkill and region is populated; should remain populated with both TrueSkills"
test2 = check_set_user("test2")
test2.region=Region.query.first()
test2.trueskills.append(TrueSkill(region="Global", mu=22, sigma=9, cons_mu=22-(9*3)))
test2.trueskills.append(TrueSkill(region=test2.region.region, mu=30, sigma=4, cons_mu=30-(4*3)))
populate_trueskills(test2)
print test2
print test2.tag, test2.trueskills
print '\n'


print "Testing update_rating"
print "test0 vs testA, Global ranking should update"
update_rating(test0, testA)
print '\n'

print "testA vs testB, Both rankings should update"
update_rating(testA, testB)
print '\n'

print "test1 vs testB, Global ranking should update"
update_rating(test1, testB)
print '\n'

print "test2 vs testB, Both rankings should update"
update_rating(test2, testB)
print '\n'

print "test2 vs testA, Both rankings should update"
update_rating(test2, testA)
print '\n'

print "test2 vs test0, Global ranking should update"
update_rating(test2, test0)
print '\n'


print "Testing reset_trueskill; all TrueSkill values should be default"
reset_trueskill(test0)
reset_trueskill(testA)
reset_trueskill(test1)
reset_trueskill(testB)
reset_trueskill(test2)
print test0
print testA
print test1
print testB
print test2


