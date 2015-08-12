from app import app, db
from app.models import *
from sort_utils import sort_setlist
from trueskill import setup, Rating, quality_1vs1, rate_1vs1

# Trueskill constants
MU = 25.0
SIGMA = 8.333333333333334
CONS_MU = 0.0
BETA = 4.166666666666667
TAU = 0.08333333333333334
DRAW_PROBABILITY = 0.0

# setup rating env
def rating_env_setup():
	setup(mu=MU, 
			sigma=SIGMA, 
			beta=BETA, 
			tau=TAU, 
			draw_probability=DRAW_PROBABILITY,
			backend=None,
			)
	return "Rating environment created"

# Given User, sets any UserSkill/TrueSkill object's trueskill to default TrueSkill object
def reset_trueskill(user):
	# if User has a TrueSkill association with a region he is not associated with, remove it
	populate_trueskills(user)

	for trueskill in user.trueskills:
		trueskill.mu = MU
		trueskill.sigma = SIGMA
		trueskill.cons_mu = CONS_MU
		db.session.commit()
	return user.trueskills

# If returns True, Global TrueSkill already populated, and Region TrueSkill to the extent of known information
def populate_trueskills(user):
	# case for when User has no TrueSkills - if User has region, populate both Global and region Trueskill
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
	elif len(user.trueskills)>=2:
		if user.region is None or user.region.region!=user.trueskills[1].region:
			user.trueskills.remove(user.trueskills[1])
			db.session.commit()
	else:
		return True

# Given two user objects representing the winner and loser of a set, update their respective ratings
def update_rating(winner_user, loser_user):
	rating_env_setup()

	# Check to see if trueskill attribute is None (new User), and if so sets it to Trueskill object with default values
	populate_trueskills(winner_user)
	populate_trueskills(loser_user)

	# Check if Users are from same region; if so, load and update Region and Global TrueSkill, else load and update Global TrueSkill
	if winner_user.region==loser_user.region and winner_user.region is not None and loser_user.region is not None:
		calc_region_trueskill(winner_user, loser_user, 1)
	else:
		calc_region_trueskill(winner_user, loser_user, 0)

	# After TrueSkills have been recalculated, commit changes and print users
	db.session.commit()

	# Exception for UnicodeError during printing, if unicode character cannot be converted, skip the print
	try:
		print winner_user, loser_user
	except UnicodeError:
		pass

	print '\n'
	return winner_user, loser_user

# given winner_user, loser_user, and integer index (0 for Region and 1 for Global), create Rating objects using currently stored Region Trueskill attribute
def calc_region_trueskill(winner_user, loser_user, region_num):
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
	winner_user.trueskills[region_num].cons_mu=new_winner_rating.mu - 3*new_winner_rating.sigma

	loser_user.trueskills[region_num].region=region_name
	loser_user.trueskills[region_num].mu=new_loser_rating.mu
	loser_user.trueskills[region_num].sigma=new_loser_rating.sigma
	loser_user.trueskills[region_num].cons_mu=new_loser_rating.mu - 3*new_loser_rating.sigma

# Reset, then recalculate all Trueskills for all Users.
def recalculate_trueskill():
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
