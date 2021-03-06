CSRF_ENABLED = True #Enables Cross-site Request Forgery. SECRET_KEY is needed when CSRF is enabled, and creates a cryptographic token used to validate a form. 
SECRET_KEY = 'you-will-never-guess'

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] 

# folder where SQLAlchemy-migrate data files will be stored
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db2_repository')

# Constants for Pagination in /views
USERS_PER_PAGE = 25
TOURNAMENTS_PER_PAGE = 15 
CHAR_USERS_PER_PAGE = 15
