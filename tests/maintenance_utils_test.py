#!flask/bin/python

from app import app, db
from app.models import *
import datetime

import sys
sys.path.append('./sanitize')
from sanitize_utils import *
from maintenance_utils import *

from trueskill import setup, Rating, quality_1vs1, rate_1vs1
from trueskill_functions import MU, SIGMA, CONS_MU, BETA, TAU, DRAW_PROBABILITY, populate_trueskills

import unittest

# Mafia has 2 characters, numbers has 1, squib
mafia = User.query.filter(User.tag=="Mafia").first()
numbers = User.query.filter(User.tag=="Infinite Numbers").first()
zoso = User.query.filter(User.tag=="Zoso").first()

class TestMaintenanceFuncs(unittest.TestCase):

	def test_character_funcs(self):
		print "\n---ADD_CHARACTER---"
		mafia.add_character("Peach")
		numbers.add_character("Ice Climbers")
		self.assertTrue(mafia.get_characters(), "Peach")
		self.assertTrue(numbers.get_characters(), "Ice Climbers")
		
		print "\n---REMOVE_CHARACTER---"
		mafia.remove_character("Peach")
		numbers.remove_character("Ice Climbers")
		self.assertTrue(mafia.get_characters(), [])
		self.assertTrue(numbers.get_characters(), [])

	def test_characterlist_funcs(self):
		print "\n---ADD_CHARACTERLIST---"
		mafia.add_characters_list(["Peach", "Captain Falcon"])
		numbers.add_characters_list(["Ice Climbers", "Yoshi"])
		self.assertTrue(mafia.get_characters(), ['Peach', 'Captain Falcon'])
		self.assertTrue(numbers.get_characters(), ['Ice Climbers', 'Yoshi'])

		print "\n---REMOVE_CHARACTERLIST---"
		mafia.remove_characters_list(['Peach', 'Captain Falcon'])
		numbers.remove_characters_list(['Ice Climbers', 'Yoshi'])
		self.assertTrue(mafia.get_characters(), ['Peach', 'Captain Falcon'])
		self.assertTrue(numbers.get_characters(), ['Ice Climbers', 'Yoshi'])


if __name__ == '__main__':
    unittest.main()