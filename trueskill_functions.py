from app import app, db
from app.models import *
from trueskill import setup, Rating, quality_1vs1, rate_1vs1

# Trueskill constants
MU = 25.0
SIGMA = 8.333333333333334
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
	for skill_assoc in user.skill_assocs:
		skill_assoc.trueskill = TrueSkill(mu=MU, sigma=SIGMA)
		db.session.commit()
	return user.skill_assocs

# If returns True, Global TrueSkill already populated, and Region TrueSkill to the extent of known information
def populate_trueskills(user):
	# case for when User has no TrueSkills - if User has region, populate both Global and region Trueskill
	if len(user.skill_assocs)<=0:
		user.skill_assocs.append(UserSkills(region="Global", trueskill=TrueSkill(mu=MU, sigma=SIGMA)))
		if user.region is not None:
			user.skill_assocs.append(UserSkills(region=user.region.region, trueskill=TrueSkill(mu=MU, sigma=SIGMA)))
	# case for when User is initialized with no region (Tournament has no region attribute during)
	# if the one regional TrueSkill is Global, and user.region is not None, populate regional TrueSkill
	elif len(user.skill_assocs)==1: 
		if user.skill_assocs[0].region=="Global" and user.region is not None:
			user.skill_assocs.append(UserSkills(region=user.region.region, trueskill=TrueSkill(mu=MU, sigma=SIGMA)))
		else:
			return True
	# If user has 2 Trueskills (Global and Region), no need to populate
	else:
		return True

# Given two user objects representing the winner and loser of a set, update their respective ratings
def update_rating(winner_user, loser_user):
	rating_env_setup()

	# Check to see if trueskill attribute is None (new User), and if so sets it to Trueskill object with default values
	populate_trueskills(winner_user)
	populate_trueskills(loser_user)

	# Check if Users are from same region; if so, load and update Region TrueSkill, else load and update Global TrueSkill
	if winner_user.region==loser_user.region:
		calc_region_trueskill(winner_user, loser_user, 1)
	else:
		calc_region_trueskill(winner_user, loser_user, 0)

	# After TrueSkills have been recalculated, commit changes and print users
	db.session.commit()
	print winner_user, loser_user
	return winner_user, loser_user

# given winner_user, loser_user, and integer index (0 for Region and 1 for Global), create Rating objects using currently stored Region Trueskill attribute
def calc_region_trueskill(winner_user, loser_user, region_num):
	winner_user_rating = Rating(winner_user.skill_assocs[region_num].trueskill.mu, winner_user.skill_assocs[region_num].trueskill.sigma)
	loser_user_rating = Rating(loser_user.skill_assocs[region_num].trueskill.mu, loser_user.skill_assocs[region_num].trueskill.sigma)
	region_name = winner_user.skill_assocs[region_num].region

	# Print current TrueSkill values for both players
	print "CURRENT TrueSkill ({0}):".format(region_name), winner_user.tag, winner_user_rating, "VS.", loser_user.tag, loser_user_rating
	
	# Record set result, victory for winner_user and loss for loser_user
	new_winner_rating, new_loser_rating = rate_1vs1(winner_user_rating, loser_user_rating)
	print "UPDATED TrueSkill ({0}):".format(region_name),  winner_user.tag, new_winner_rating, "VS.", loser_user.tag, new_loser_rating

	# Store and overwrite existing trueskill object with new Rating values
	winner_user.skill_assocs[region_num].trueskill = TrueSkill(mu=new_winner_rating.mu, sigma=new_winner_rating.sigma)
	loser_user.skill_assocs[region_num].trueskill = TrueSkill(mu=new_winner_rating.mu, sigma=new_winner_rating.sigma)
