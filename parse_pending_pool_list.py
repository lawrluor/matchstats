#! flask/bin/python

from app import app, db
from app.models import *
from parse_challonge_run import *

parse_challonge_pool("http://challonge.com/HUSHPool1", "HUSH (Pro)", "New England", 2)
parse_challonge_pool("http://challonge.com/HUSHPool2", "HUSH (Pro)", "New England", 2)
parse_challonge_pool("http://challonge.com/HUSHPool3", "HUSH (Pro)", "New England", 2)
parse_challonge_pool("http://challonge.com/HUSHPool4", "HUSH (Pro)", "New England", 2)