#!flask/bin/python
#Currently only supports APEX 2015 Top 8 Results: Current as of June 25 2015, 4:28 PM
import os
import unittest

from config import basedir
from app import app, db
from app.models import *
from h2h_stats_functions import *

# THIS TEST IS OBSOLETE

userlist = User.query.all()
setlist = Set.query.all()
matchlist = Match.query.all()

print userlist
print '\n'
print setlist
print '\n'
print matchlist

print "Testing User connections to Set"
PPMD = userlist[0]
Armada = userlist[1]
Leffen = userlist[2]
Mango = userlist[3]
Hungrybox = userlist[4]
aMSa = userlist[5]
KirbyKaze = userlist[6]
Shroomed = userlist[7]
print '\n'

print "Testing User.getWonSets"
shroomed_won_sets = Shroomed.getWonSets()
print shroomed_won_sets
hungrybox_won_sets = Hungrybox.getWonSets()
print hungrybox_won_sets
print '\n'


print "Testing User.getLostSets"
kirbykaze_lost_sets = KirbyKaze.getLostSets()
print kirbykaze_lost_sets
aMSa_lost_sets = aMSa.getLostSets()
print aMSa_lost_sets
print '\n'

print "Testing User.getAllSets()"
PPMD_all_sets = PPMD.getAllSets()
print PPMD_all_sets
Leffen_all_sets = Leffen.getAllSets()
print Leffen_all_sets
print '\n'

print "Testing Set connections to User"
hungrybox_shroomed = setlist[0]
aMSa_kirbykaze = setlist[1]
PPMD_armada = setlist[2]
leffen_mango = setlist[3]
armada_hungrybox = setlist[4]
mango_aMSa = setlist[5]
armada_mango = setlist[6]
PPMD_leffen = setlist[7]
armada_leffen = setlist[8]
armada_PPMD_GF1 = setlist[9]
PPMD_armada_GF2 = setlist[10]
print '\n'

print "Testing Set.getSetWinner()"
print hungrybox_shroomed.getSetWinner()
print aMSa_kirbykaze.getSetWinner()
print '\n'

print "Testing Set.getSetWinnerID()"
print hungrybox_shroomed.getSetWinnerID()
print aMSa_kirbykaze.getSetWinnerID()
print '\n'

print "Testing Set.getSetLoser()"
print leffen_mango.getSetLoser()
print PPMD_armada.getSetLoser()
print '\n'

print "Testing Set.getSetLoserID"
print leffen_mango.getSetLoserID()
print PPMD_armada.getSetLoserID()
print '\n'

print "Testing Set and Matches relationship"
print armada_PPMD_GF1.matches.all()
print '\n'
print "PPMD match wins"
print armada_PPMD_GF1.matches.filter(Match.winner==PPMD.tag).all()
print armada_PPMD_GF1.matches.filter(Match.winner==PPMD.tag).count()
print '\n'
print "Armada match wins"
print armada_PPMD_GF1.matches.filter(Match.winner==Armada.tag).all()
print armada_PPMD_GF1.matches.filter(Match.winner==Armada.tag).count()
print '\n'


print "Testing Head to Head functions"
print "Testing h2h_get_sets_played(Armada.tag, PPMD.tag)"
h2h_sets_played = h2h_get_sets_played(Armada.tag, PPMD.tag)
print h2h_sets_played
print '\n'
print "Testing h2h_get_sets_won(PPMD.tag, Armada.tag)"
print h2h_get_sets_won(PPMD.tag, Armada.tag)
print '\n'
print "Testing h2h_get_sets_won(Armada.tag, PPMD.tag)"
print h2h_get_sets_won(Armada.tag, PPMD.tag)
print '\n'

print "Testing h2h_get_matches_played(h2h_sets_played)"
h2h_matches_played = h2h_get_matches_played(h2h_sets_played)
print h2h_matches_played
print '\n'
print "Testing h2h_get_matches_won(PPMD.tag, Armada.tag, h2h_matches_played)"
print h2h_get_matches_won(PPMD.tag, Armada.tag, h2h_matches_played)
print '\n'
print "Testing h2h_get_matches_won(Armada.tag, PPMD.tag, h2h_matches_played)"
print h2h_get_matches_won(Armada.tag, PPMD.tag, h2h_matches_played)
print '\n'

print "Testing h2h_get_stages_played"
Stages = h2h_get_stages_played(h2h_matches_played)
print Stages
print'\n'
print "Testing h2h_get_stages_won"
print h2h_get_stages_won(PPMD.tag, Stages)
print '\n'

print "Testing h2h_get_character_played(PPMD.tag, Marth, h2h_matches_played)"
PPMD_marth_matches = h2h_get_character_played(PPMD.tag, 'Marth', h2h_matches_played)
print PPMD_marth_matches
print '\n'
print "Testing h2h_character_wins(PPMD.tag, PPMD_marth_matches)"
print h2h_character_wins(PPMD.tag, PPMD_marth_matches)
print '\n'


#clear non APEX 2015 users, sets, and matches
for user in userlist[8:]:
	db.session.delete(user)

for set in setlist[11:]:
	db.session.delete(set)

for match in matchlist[47:]:
	db.session.delete(match)

db.session.commit()