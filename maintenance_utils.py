from app import app, db
from app.models import *

import sys
sys.path.append('./sanitize')
from sanitize_utils import check_and_sanitize_tag

from trueskill import setup, Rating, quality_1vs1, rate_1vs1
from trueskill_functions import MU, SIGMA, BETA, TAU, DRAW_PROBABILITY, populate_trueskills

# Given a User tag and region name, changes user.region and changes regional trueskill if region is valid, otherwise deletes it
def change_region(tag, region_name):
  user = User.query.filter(User.tag==tag).first()
  region = Region.query.filter(Region.region==region_name).first()

  if user.region is not None and user.region.region==region_name:
    return "Region %s is already region of %s" % (region_name, tag)
  user.region = region
  
  # Repopulate regional trueskill for new region, to the default. First call deletes obsolete region, second call repopulates regional trueskill with new region. 
  # If new region is None, deletes obsolete region and does nothing else
  # If user.region was already None, does nothing
  populate_trueskills(user)
  populate_trueskills(user)

  return user
