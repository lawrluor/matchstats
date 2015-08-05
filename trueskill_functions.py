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

	# create Rating objects using currently stored trueskill attribute
	winner_user_rating = Rating(winner_user.trueskill.mu, winner_user.trueskill.sigma)
	loser_user_rating = Rating(loser_user.trueskill.mu, loser_user.trueskill.sigma)
	print winner_user.tag, winner_user_rating, " | ", loser_user.tag, loser_user_rating

	# Simulate a victory for winner_user
	new_winner_rating, new_loser_rating = rate_1vs1(winner_user_rating, loser_user_rating)
	print "updated trueskill", winner_user.tag, new_winner_rating, " | ", "updated trueskill", loser_user.tag, new_loser_rating

	# Store and overwrite existing trueskill object with new Rating values
	winner_user.trueskill = TrueSkill(mu=new_winner_rating.mu, sigma=new_winner_rating.sigma)
	loser_user.trueskill = TrueSkill(mu=new_loser_rating.mu, sigma=new_loser_rating.sigma)
	print winner_user, loser_user
	print '\n'

	db.session.commit()

	return winner_user, loser_user
