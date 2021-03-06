from app import app, db
from app.models import *
from sort_utils import sort_setlist
from misc_utils import print_ignore
import time
from trueskill import setup, Rating, quality_1vs1, rate_1vs1

# Trueskill constants for rating environment setup
MU = 25
SIGMA = 8.333333333333334
STD = 1
CONS_MU = MU - (STD*SIGMA)
BETA = 4.166666666666667
TAU = 0.08333333333333334
DRAW_PROBABILITY = 0.0

# Not used in these functions
def rating_env_setup():
  """Sets up Rating Environment, an object from trueskill module.

  Args:
    None, but setup uses Global variables defined above.

  Returns:
    Global env created=
  """
  global_env = setup(mu=MU, 
			sigma=SIGMA, 
			beta=BETA, 
			tau=TAU, 
			draw_probability=DRAW_PROBABILITY,
			backend=None
			)
  return global_env

def reset_trueskill(user):
	"""Given User, sets associated TrueSkill objects' values to default.

  Args:
    user: A User object.

  Returns:
    The TrueSkill objects associated with a User.
	"""

	# remove TrueSkill association with a region if User is not associated with it anymore 
	populate_trueskills(user)

	for trueskill in user.trueskills:
		trueskill.mu = MU
		trueskill.sigma = SIGMA
		trueskill.cons_mu = CONS_MU
	db.session.commit()
	return user.trueskills

def reset_all_trueskills():
	# Reset all User Trueskill to defaults
	userlist = User.query.all()
	for user in userlist:
		reset_trueskill(user)

def populate_trueskills(user):
	"""Populates TrueSkill associations of User

	Args:
  	user: A User object.
  
 	Returns:
  	If User already has Global and appropriate Regional TrueSkill, returns True.
  	Adds TrueSkill association for Global if it does not already exist.
  	Deletes TrueSkill association for Region if User no longer is associated with that region.
	"""
	
	# case for when User has no TrueSkills; if User has region, populate both Global and region Trueskill
	if len(user.trueskills)<=0:
		user.trueskills.append(TrueSkill(region="Global", mu=MU, sigma=SIGMA, cons_mu=CONS_MU))
		if user.region is not None:
			user.trueskills.append(TrueSkill(region=user.region.region, mu=MU, sigma=SIGMA, cons_mu=CONS_MU))
	# case for when User is initialized with no region (Tournament has no region attribute during)
	# if the one regional TrueSkill is Global, and user.region is not None, populate regional TrueSkill
	elif len(user.trueskills)==1: 
		if user.trueskills[0].region=="Global" and user.region is not None:
			user.trueskills.append(TrueSkill(region=user.region.region, mu=MU, sigma=SIGMA, cons_mu=CONS_MU))
			db.session.commit()
		else:
			return True
	# If User has 2 Trueskills (Global and Region), check to make sure he should have a regional TrueSkill (if he belongs to a region)
  # if User Region does not match TrueSkill region, remove it
	elif len(user.trueskills)>=2:
		if user.region is None or user.region.region!=user.trueskills[1].region:
			user.trueskills.remove(user.trueskills[1])
			db.session.commit()
	else:
		return True

def update_rating(winner_user, loser_user):
	"""
	Update ratings of two Users who played a Set.

	Args:
  	winner_user: A User object representing winner of the set.
  	loser_user: A User object representing loser of the set.

  	Returns:
  	A tuple of the Winner and Loser of the Set, both User objects, with updated
  	TrueSkills. This value is never used.
	"""

	# Check to see if trueskill attribute is None (new User), and if so sets it to Trueskill object with default values
	populate_trueskills(winner_user)
	populate_trueskills(loser_user)

	# Check if Users are from same region; if so, load and update Region and Global TrueSkill, else load and update Global TrueSkill
	if winner_user.region==loser_user.region and winner_user.region is not None and loser_user.region is not None:
		calc_region_trueskill(winner_user, loser_user, 1)
	else:
		calc_region_trueskill(winner_user, loser_user, 0)
	print '\n'

	# After TrueSkills have been recalculated, commit changes and print users
	db.session.commit()
	return winner_user, loser_user

def calc_region_trueskill(winner_user, loser_user, region_num):
	"""Recalculates regional TrueSkill association between Users depending on
	Region the Set was played in

	Args:
  	winner_user: A User object representing winner of Set
  	loser_user: A User object representing loser of Set
  	region_num: An integer, index of User.trueskills (0 for Region and 1 for Global)

	Returns:
  	None.
	"""  

	# Create Rating objects using currently stored Region Trueskill attribute
	winner_user_rating = Rating(winner_user.trueskills[region_num].mu, winner_user.trueskills[region_num].sigma)
	loser_user_rating = Rating(loser_user.trueskills[region_num].mu, loser_user.trueskills[region_num].sigma)
	region_name = winner_user.trueskills[region_num].region

	# Print current TrueSkill values for both players
	print "CURRENT TrueSkill ({0}):".format(region_name), winner_user.tag, winner_user_rating, "VS.", loser_user.tag, loser_user_rating
	
	# Record set result, victory for winner_user and loss for loser_user
	new_winner_rating, new_loser_rating = rate_1vs1(winner_user_rating, loser_user_rating)
	print "UPDATED TrueSkill ({0}):".format(region_name),  winner_user.tag, new_winner_rating, "VS.", loser_user.tag, new_loser_rating

	# Store and overwrite existing trueskill object with new Rating values
	winner_user.trueskills[region_num].region=region_name
	winner_user.trueskills[region_num].mu=new_winner_rating.mu
	winner_user.trueskills[region_num].sigma=new_winner_rating.sigma
	winner_user.trueskills[region_num].cons_mu=new_winner_rating.mu - STD*new_winner_rating.sigma

	loser_user.trueskills[region_num].region=region_name
	loser_user.trueskills[region_num].mu=new_loser_rating.mu
	loser_user.trueskills[region_num].sigma=new_loser_rating.sigma
	loser_user.trueskills[region_num].cons_mu=new_loser_rating.mu - STD*new_loser_rating.sigma

def recalculate_trueskill():
	"""Resets, then recalculates all Trueskills for all Users.
	
	Args:
		None

	Returns:
		String indicating success. This value is never used.
	"""
	# Iterate through all Sets in order and recalculate Trueskill; currently in order of set.id
	# order Sets by tournament date, then by set id, oldest being at index 0
	setlist = Set.query.all()
	sorted_setlist = sort_setlist(setlist)

	# BUG: if user.tag changed for a User, the Set winner/loser tag will still remain, so when querying for User using the Set's outdated tag, queried User becomes None.
	# Solution: Check and sanitize winner_tag, loser_tag again. But if it wasn't recognized in the first place, still an issue
	# This takes a long time to run. How to optimize?
	for set in sorted_setlist:
		winner_user = User.query.filter(User.tag==set.winner_tag).first()
		loser_user = User.query.filter(User.tag==set.loser_tag).first()
		update_rating(winner_user, loser_user)
		print sorted_setlist.index(set)
	print "All trueskills recalculated"

def trueskills_dict():
	'''
	Returns a dictionary with every user represented as a dictionary key User.tag
	Dictionary values are the user's corresponding Trueskills
	'''
	skills_by_user = {}
	userlist = User.query.all()
	for user in userlist:
		print_ignore(user.tag)

		# Check to see if trueskill attribute is None (new User), and if so sets it to Trueskill object with default values
		populate_trueskills(user)

		# Assign value to user key, the corresponding list of User's Trueskills
		skills_by_user[user.tag] = user.trueskills
		print_ignore(skills_by_user[user.tag])
	return skills_by_user


def update_rating_dict(winner_user, loser_user, skills_dict):
	"""
	Update ratings of trueskill values stored in dict representing User trueskills who played a Set
	Called from recalculate_trueskills_dict()

	Args:
  	winner_user: A User object representing winner of the set.
  	loser_user: A User object representing loser of the set.

  	Returns:
  	A tuple of the Winner and Loser of the Set, both User objects, with updated
  	TrueSkills. This value is never used.
	"""

	# Check if Users are from same region; if so, load and update Region and Global TrueSkill, else load and update Global TrueSkill
	if winner_user.region==loser_user.region and winner_user.region is not None and loser_user.region is not None:
		calc_region_trueskill_dict(winner_user, loser_user, 1, skills_dict)
	else:
		calc_region_trueskill_dict(winner_user, loser_user, 0, skills_dict)
	print '\n' 
	return skills_dict[winner_user.tag], skills_dict[loser_user.tag]

def calc_region_trueskill_dict(winner_user, loser_user, region_num, skills_dict):
	# Create Rating objects using currently stored Region Trueskill attribute
	winner_user_rating = Rating(skills_dict[winner_user.tag][region_num].mu, skills_dict[winner_user.tag][region_num].sigma)
	loser_user_rating = Rating(skills_dict[loser_user.tag][region_num].mu, skills_dict[loser_user.tag][region_num].sigma)
	region_name = skills_dict[winner_user.tag][region_num].region

	# Print current TrueSkill values for both players
	print "CURRENT TrueSkill ({0}):".format(region_name), winner_user.tag, winner_user_rating, "VS.", loser_user.tag, loser_user_rating
	
	# Record set result, victory for winner_user and loss for loser_user
	new_winner_rating, new_loser_rating = rate_1vs1(winner_user_rating, loser_user_rating)
	print "UPDATED TrueSkill ({0}):".format(region_name),  winner_user.tag, new_winner_rating, "VS.", loser_user.tag, new_loser_rating

	# Store and overwrite existing trueskill object with new Rating values
	skills_dict[winner_user.tag][region_num].region=region_name
	skills_dict[winner_user.tag][region_num].mu=new_winner_rating.mu
	skills_dict[winner_user.tag][region_num].sigma=new_winner_rating.sigma
	skills_dict[winner_user.tag][region_num].cons_mu=new_winner_rating.mu - STD*new_winner_rating.sigma

	skills_dict[loser_user.tag][region_num].region=region_name
	skills_dict[loser_user.tag][region_num].mu=new_loser_rating.mu
	skills_dict[loser_user.tag][region_num].sigma=new_loser_rating.sigma
	skills_dict[loser_user.tag][region_num].cons_mu=new_loser_rating.mu - STD*new_loser_rating.sigma

def assign_trueskills_dict(skills_dict):
	for user_key in skills_dict:
		user = User.query.filter(User.tag==user_key).first()
		user.trueskills = skills_dict[user_key]
	return skills_dict

def recalculate_trueskills_dict():
	# Generate dictionary with User.tag as key, User.trueskills as values
	skills_dict = trueskills_dict()

	# Iterate through all Sets in order and recalculate Trueskill; currently in order of set.id
	# order Sets by tournament date, then by set id, oldest being at index 0
	setlist = Set.query.all()
	sorted_setlist = sort_setlist(setlist)

	for set in sorted_setlist:
		winner_user = User.query.filter(User.tag==set.winner_tag).first()
		loser_user = User.query.filter(User.tag==set.loser_tag).first()
		update_rating_dict(winner_user, loser_user, skills_dict)
		# print set.index()

	assign_trueskills_dict(skills_dict)
	print "All trueskills recalculated"
	return skills_dict

def debug_trueskills_dict(skills_dict):
	errors = 0
	for user_key in skills_dict:
		user = User.query.filter(User.tag==user_key).first()
		if user.trueskills==skills_dict[user_key]:
			print True
		else:
			print False
			print user
			errors += 1
	return "Errors:", errors

def recalculate_ranks(region_name):
	userlist = User.query.join(User.trueskills).filter(TrueSkill.region==region_name).order_by(TrueSkill.cons_mu.desc()).all()
	if userlist is None:
		return "Region not Found"

	for i in range(len(userlist)):
		user = userlist[i]
		if region_name=="Global":
			user.trueskills[0].rank = i + 1
		else:
			user.trueskills[1].rank = i + 1

	db.session.commit()
	return userlist
