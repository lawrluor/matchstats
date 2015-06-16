#Currently returns index template  to be displayed on client's web browser. Routes map URLs to the function.

from flask import render_template #takes template filename and variable list of template arguments and returns rendered template with arguments replaced.
from app import app

@app.route('/')
@app.route('/index')
def index():
  user = {'tag' : 'Law' } #fake fuck
  return render_template('index.html',
                        title ='Home',
                        user=user)


@app.route('/login') #login page for user
def login():
  return "You are currently at: login page"

@app.route('/browse') #browse recent tournaments and matches
def browse():
  user = {'tag' : 'Law' }
  recent_sets = [{
                'player1' : {'tag' : 'Tonic'},
                'player2' : {'tag' : 'Wyne'},
                'result' : 'Tonic beats  Wyne (69-0)'
                },
                {
                'player1' : {'tag' : 'M2k'},
                'player2' : {'tag' : 'Plup'},
                'result' : 'M2K beats Plup (3-0)'
                }]
  return render_template("browse.html",
                         title='Browse',
                         user=user,
                         recent_sets=recent_sets)
  
@app.route('/user/<tag>') #arbitrary user profile page. login currently not required.
def user(tag):
  user = {'tag' : 'Law' }
  user_sets = [{
              'player1' : {'tag' : 'Law'},
              'player2' : {'tag' : 'Rye'},
              'result' : 'Law beats Rye (9001-0)'
              }]
  return render_template("user.html",
                        title=tag,
                        user=user,
                        user_sets=user_sets)


@app.route('/edit') #edit self user profile page. login will be necessary
def edit():
  return "You are currently at: profile edit page"
