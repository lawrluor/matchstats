from flask import Flask

#Creates application object (of class Flask) and imports views module. app the object is different from the "from app" package.

app = Flask(__name__)
from app import views
