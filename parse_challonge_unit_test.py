#!flask/bin/python
#Currently using fake setlist item

import os
import unittest

from config import basedir
from app import app, db
from app.models import *
from parse_challonge import *

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

Tournament = "CEO 2014"

# Get: score, tag, seed, round
for set in setlist:
	top_player = set[0]
	bottom_player = set[1]

	# Determine the set winner and loser based on their scores. Once assigned, no more references 
	# will be made to the ambiguous top and bottom player, but instead to set_winner and set_loser
	# Both set_winner and set_loser are DICTIONARIES. Scores are stored in respective variables
	if top_player['score'] > bottom_player['score']:
		set_winner = top_player
		set_loser = bottom_player
		winner_score = top_player['score']
		loser_score = bottom_player['score']
	else:
		set_winner = bottom_player
		set_loser = top_player
		winner_score = bottom_player['score']
		loser_score = top_player['score']

	# After calling this function, Users by 'tag' will exist in database in any case.
	# stores User object in respective variables
	winner_user = check_set_user(set_winner['tag'])
	loser_user = check_set_user(set_loser['tag'])

	print winner_user
	print loser_user

	# If seed doesn't exist, do nothing; else, assign to User attribute seed
	if set_winner['seed']:
		winner_user.seed = set_winner['seed']
	if set_loser['seed']:
		loser_user.seed = set_loser['seed']

	# Get round number; if they match, store the round variable; if they don't (some error occurred), ignore it.
	if int(set_winner['round']) == int(set_loser['round']):
		round_number = int(set_winner['round'])
	else:
		# prevent crashing when creating the Set without existing variable round_number
		round_number = 0

	# Convert scores to integers

	new_set = Set(tournament=Tournament,
								round_type=round_number,
								winner_tag=winner_user.tag,
								loser_tag=loser_user.tag,
								winner_id=winner_user.id,
								loser_id=loser_user.id,
								winner_score=winner_score,
								loser_score=loser_score,
								total_matches=winner_score+loser_score)

	db.session.add(new_set)
	print new_set
	print '\n'

db.session.commit()

print "Printing Userlist and Setlist"
userlist = User.query.all()
for user in userlist:
	print user
print '\n'

setlist = Set.query.all()
for set in setlist:
	print set
print '\n'