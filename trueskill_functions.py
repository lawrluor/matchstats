from app import app, db
from app.models import *
from sort_utils import sort_setlist
from misc_utils import print_ignore
from trueskill import setup, Rating, quality_1vs1, rate_1vs1

# Trueskill constants for rating environment setup
MU = 25
SIGMA = 8.333333333333334
STD = 2.25
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
	"""Update ratings of two Users who played a Set.

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

  #  Create Rating objects using currently stored Region Trueskill attribute
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
	# Reset all User Trueskill to defaults
	userlist = User.query.all()
	for user in userlist:
		reset_trueskill(user)

	# Iterate through all Sets in order and recalculate Trueskill; currently in order of set.id
	# order Sets by tournament date, then by set id, oldest being at index 0
	setlist = Set.query.all()
	sorted_setlist = sort_setlist(setlist)

	# BUG: if user.tag changed for a User, the Set winner/loser tag will still remain, so when querying for User using the Set's outdated tag, queried User becomes None.
	# Solution: Check and sanitize winner_tag, loser_tag again. But if it wasn't recognized in the first place, still an issue
	for set in sorted_setlist:
		winner_user = User.query.filter(User.tag==set.winner_tag).first()
		loser_user = User.query.filter(User.tag==set.loser_tag).first()
		update_rating(winner_user, loser_user)

	print "All trueskills recalculated"
