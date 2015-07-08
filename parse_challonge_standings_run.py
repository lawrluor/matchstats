#!flask/bin/python

from app import app, db
from app.models import *

import urllib3
from bs4 import BeautifulSoup
import re

import sys

from parse_challonge_standings import *

def main():
  parse_challonge_standings(sys.argv[1])
  parse_challonge_info(sys.argv[1])

if __name__ == "__main__":
	main()
