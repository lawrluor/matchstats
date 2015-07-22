from app import app, db
from app.models import *
from trueskill import setup, Rating, quality_1vs1, rate_1vs1

# setup rating env
def rating_env_setup():
	setup(mu=25.0, 
			sigma=8.333333333333334, 
			beta=4.166666666666667, 
			tau=0.08333333333333334, 
			draw_probability=0.0,
			backend=None,
			)
	return "Rating environment created"

# Given user object, if trueskill attribute is None, sets attribute to a created Trueskill object
def check_trueskill(user):
	if user.trueskill is None:
		user.trueskill = TrueSkill(mu=25.0, sigma=8.333333333333334)
		db.session.commit()
	print user.trueskill
	return user.trueskill

# Given two user objects representing the winner and loser of a set, update their respective ratings
def update_rating(winner_user, loser_user):
	rating_env_setup()

	# Check to see if trueskill attribute is None (new User), and if so sets it to Trueskill object with default values
	check_trueskill(winner_user)
	check_trueskill(loser_user)

	# create Rating objects using currently stored trueskill attribute
	winner_user_rating = Rating(winner_user.trueskill.mu, winner_user.trueskill.sigma)
	loser_user_rating = Rating(loser_user.trueskill.mu, loser_user.trueskill.sigma)
	print winner_user_rating, loser_user_rating

	# Simulate a victory for winner_user
	new_winner_rating, new_loser_rating = rate_1vs1(winner_user_rating, loser_user_rating)
	print new_winner_rating, new_loser_rating
	print '\n'

	# Store and overwrite existing trueskill object with new Rating values
	winner_user.trueskill = TrueSkill(mu=new_winner_rating.mu, sigma=new_winner_rating.sigma)
	loser_user.trueskill = TrueSkill(mu=new_loser_rating.mu, sigma=new_loser_rating.sigma)
	print winner_user, loser_user

	db.session.commit()
	return winner_user, loser_user
