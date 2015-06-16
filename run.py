#!flask/bin/python
from app import app
app.run(debug=True)

#Imports app variable which holds the Flask object (in __init__.py) from the app package and invokes its run method to start the server.
