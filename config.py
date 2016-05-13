CSRF_ENABLED = True #Enables Cross-site Request Forgery. SECRET_KEY is needed when CSRF is enabled, and creates a cryptographic token used to validate a form. 
SECRET_KEY = 'you-will-never-guess'

import os
basedir = os.path.abspath(os.path.dirname(__file__))
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] 

# folder where SQLAlchemy-migrate data files will be stored
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db2_repository')

# Constants for Pagination in /views
USERS_PER_PAGE = 25
TOURNAMENTS_PER_PAGE = 15 
CHAR_USERS_PER_PAGE = 15
