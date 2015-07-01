#!flask/bin/python

from app import app, db
from app.models import *
from app.views import *
import sys

def main():
	print User.query.filter(User.tag=='C9 Mang0').first()
	make_same_user(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
	main()