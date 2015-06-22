# Currently returns index template to be displayed on client's web browser. Routes map URLs to the function.

from flask import render_template, flash, redirect, request, url_for
from app import app, db
from models import User, Set, Match
from forms import UserCreate, SetCreate, MatchSubmit, HeadToHead
from sqlalchemy import and_

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html',
                        title ='Home')


@app.route('/browse_sets') # browse sets
def browse_sets():
  setlist = Set.query.all()
  return render_template("browse_sets.html",
                         title='Browse Sets',
                         setlist=setlist)


@app.route('/browse_users') # browse users
def browse_users():
  userlist = User.query.all()
  return render_template("browse_users.html",
                        title='Browse Users',
                        userlist=userlist)


@app.route('/user_create', methods=['GET', 'POST']) # 'POST' allows us to receive POST requests, which will bring in form data entered by the user
def user_create():
  form = UserCreate() # instantiate object from UserCreate() class in app/forms.py
  if form.validate_on_submit(): # if True, indicates data is valid and can be processed
    created_tag = form.user_tag.data # stores entered value in variable
    created_region = form.user_region.data
    created_main = form.user_main.data

    
    # create user row, initializing user object
    new_user = User(tag=created_tag,
                main=created_main,
                region=created_region)

    # commit to db
    db.session.add(new_user)
    db.session.commit()
    flash('User creation successful.')

    return redirect('/index')
  return render_template('user_create.html', # renders template for creating user if called before user enters data
                        title='Create User',
                        form=form)


@app.route('/set_create', methods=['GET', 'POST']) # 'POST' allows us to receive POST requests, which will bring in form data entered by the user
def set_create():
  form = SetCreate() # instantiate object from SetCreate() class in app/forms.py
  if form.validate_on_submit(): # if True, indicates data is valid and can be processed
    # Based on winner and loser tag submitted through form, queries User database to locate the respective Users
    set_winner = User.query.filter(User.tag==form.set_winner_tag.data).first() 
    set_loser = User.query.filter(User.tag==form.set_loser_tag.data).first()
    
    set_winner_tag = form.set_winner_tag.data
    set_loser_tag = form.set_loser_tag.data
    set_winner_id = set_winner.id
    set_loser_id = set_loser.id

    created_set_winner_score = form.set_winner_score.data
    created_set_loser_score = form.set_loser_score.data
    created_total_matches = created_set_loser_score + created_set_winner_score
    created_max_match_count = int(form.set_max_match_count.data)
   
    # Check to see if set score count is valid for type of set, and winner score>loser score
    if ((created_set_winner_score <= created_set_loser_score) or 
      ((created_set_winner_score > ((created_max_match_count / 2.0) + 1)) or 
      (created_set_winner_score < (created_max_match_count / 2.0)))):
      
      flash("Check to make sure you have entered the appropriate scores for the set score cout.")
      return redirect(url_for('set_create'))

    # create set row, initializing set object
    new_set = Set(
                  winner_tag=set_winner_tag,
                  loser_tag=set_loser_tag,
                  winner_id=set_winner_id,
                  loser_id=set_loser_id,
                  winner_score=created_set_winner_score,
                  loser_score=created_set_loser_score,
                  max_match_count=created_max_match_count,
                  total_matches=created_total_matches
                  )
    
    # Add winner_id and loser_id attributes for Set; must be done after creating the Set object so that it can call the getSetWinnerID and getSetLoserID functions
    new_set.winner_id = new_set.getSetWinnerID()
    new_set.loser_id = new_set.getSetLoserID()

    # commit to db
    db.session.add(new_set)
    db.session.commit()
    flash('Next, enter data for the individual matches.') # if Set is created successfully, redirect to the match_create page, where data for individual matches entered

    return redirect(url_for('match_submit', set_id=str(new_set.id), total_matches=int(new_set.total_matches)))
  return render_template('set_create.html', # renders template for creating user if called before user enters data
                        title='Create Set', 
                        form=form
                        )

@app.route('/match_submit', methods=['GET', 'POST'])
def match_submit(): # set_id, total_matches passed through url from route /set_create as query strings automatically because they weren't passed as parameters of match_sbumit or part of the route /match_submit
 
  set_id = request.args.get('set_id')
  total_matches = request.args.get('total_matches')
  
  form = MatchSubmit() # instantiate object from MatchSubmit() class in app/forms.py
  if form.validate_on_submit():
    submitted_match_stage = form.match_stage.data
    submitted_match_winner = form.match_winner.data
    submitted_match_loser = form.match_loser.data
    submitted_winner_char = form.winner_char.data
    submitted_loser_char = form.loser_char.data


    new_match = Match(stage=submitted_match_stage,
                      winner=submitted_match_winner,
                      loser=submitted_match_loser,
                      winner_char=submitted_winner_char,
                      loser_char=submitted_loser_char,
                      set_id=set_id 
                      )
    
    # commit to db
    db.session.add(new_match)
    db.session.commit()
    
    # code for submitting the next match in the set
    total_matches = int(total_matches) - 1 # now that one match has been submitted, there is one less match to be submitted out of the total number initially indicated when set was created
    if total_matches == 0: # base case: if no more matches to submit, redirected home
      flash('Submission Complete') 
      return redirect('/index')
    else:
      total_matches = str(total_matches) # necessary to convert again for flash message and more importantly as a parameter of function match_submit
      flash('Match Submission Complete. Submit next Match. Matches left: ' + total_matches)
      return redirect(url_for('match_submit', set_id=set_id, total_matches=total_matches))

  return render_template('match_submit.html',
                          title='Submit Match',
                          form=form)


@app.route('/user/<tag>') # User profile page
def user(tag):
  user = User.query.filter(User.tag==tag).first() # If routed to user profile page (user/<tag>), check to make sure user exists
  if user is None:
    flash('User %s not found.' % tag)
    return redirect(url_for('index'))
  user_sets = user.getAllSets() # Store all user's sets in variable user_sets
  user_lost_sets = user.getLostSets()
  user_won_sets = user.getWonSets()
  return render_template("user.html",
                        title=tag,
                        user=user,
                        user_sets=user_sets,
                        user_lost_sets=user_lost_sets,
                        user_won_sets=user_won_sets) # pass user's sets in variable user_sets  to form user.html 


# Head to Head page to begin querying User head to head 
@app.route('/head_to_head', methods=['GET', 'POST'])
def head_to_head():
  form = HeadToHead()
  if form.validate_on_submit():
    user1 = form.user1.data
    user2 = form.user2.data

    valid_users = User.query.filter(User.tag==user1).all()
    valid_users = valid_users + User.query.filter(User.tag==user2).all()

    if len(valid_users) < 2:
      flash('At least one User not found.')
      return redirect(url_for('head_to_head'))
    
    return redirect(url_for('versus', user1=user1, user2=user2))

  return render_template("head_to_head.html",
                        form=form)
                         

#  User head to head page
@app.route('/versus')
def versus():
  tag1 = request.args.get('user1')
  tag2 = request.args.get('user2')

  # Get all sets that user1 and user2 have played
  sets = Set.query.filter(and_(Set.winner_tag==tag1, Set.loser_tag==tag2)).all()
  sets = sets + Set.query.filter(and_(Set.winner_tag==tag2, Set.loser_tag==tag1)).all()
  
  return render_template("versus.html",
                         tag1=tag1,
                         tag2=tag2,
                         setlist=sets)


@app.route('/region/<region>') # View all users in certain region
def view_region(region):
  users = User.query.filter(User.region==region).all() # checks to see if user.region is identical to region
  if user is None:
    flash('No players found in this region') # no user found with matching region
  return render_template("view_region.html",
                         users=users,
                         region=region)

# During production mode (runp.py), debug is turned OFF and these error templates appear
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
