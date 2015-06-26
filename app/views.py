# Currently returns index template to be displayed on client's web browser. Routes map URLs to the function.

from flask import render_template, flash, redirect, request, url_for
from app import app, db
from models import User, Set, Match, Character, secondaries
from forms import UserCreate, UserEdit, SetCreate, MatchSubmit, HeadToHead, main_char_choices, secondaries_char_choices, main_char_list, secondaries_char_list
from sqlalchemy import and_


@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html',
                        title ='Home')


@app.route('/user_create', methods=['GET', 'POST']) # 'POST' allows us to receive POST requests, which will bring in form data entered by the user
def user_create():
  form = UserCreate() # instantiate object from UserCreate() class in app/forms.py
  if form.validate_on_submit(): # if True, indicates data is valid and can be processed
    created_tag = form.user_tag.data # stores entered value in variable
    created_region = form.user_region.data
    created_main = form.user_main.data
    created_secondaries = form.user_secondaries.data

    # create user row, initializing user object
    new_user = User(tag=created_tag,
                main=created_main,
                region=created_region
                )

    # commit to db
    db.session.add(new_user)
    db.session.commit()
    flash('User creation successful.')
    
    # now add secondaries to User
    new_user.add_secondaries_list(created_secondaries)
    db.session.commit()

    flash('Secondaries added to User.')
    return redirect('/browse_users')

  return render_template('user_create.html', # renders template for creating user if called before user enters data
                        title='Create User',
                        form=form)

@app.route('/user_edit/<user>', methods=['GET', 'POST'])
def user_edit(user):
  form = UserEdit()
  current_user = User.query.filter(User.tag==user).first() 
  current_secondaries = current_user.get_secondaries() 

  form.add_secondaries.choices = [(x, x) for x in secondaries_char_list if x != current_user.main and x not in current_secondaries] 
  form.remove_secondaries.choices = [(x, x) for x in current_secondaries] 

  if form.validate_on_submit():
    current_user.tag = form.edit_tag.data
    current_user.region = form.edit_region.data
    current_user.main = form.edit_main.data
    add_characterlist = form.add_secondaries.data
    remove_characterlist = form.remove_secondaries.data

    current_user.add_secondaries_list(add_characterlist)
    current_user.remove_secondaries_list(remove_characterlist)
    
    db.session.commit()
    flash('Changes have been saved.')
    # important that it's the raw data, otherwise redirect will fail if user tag is changed
    return redirect(url_for('user', tag=form.edit_tag.data))
  
  # populate forms prior to rendering template
  else:
    form.edit_tag.data = current_user.tag
    form.edit_region.data = current_user.region
    form.edit_main.data = current_user.main

  return render_template('user_edit.html',
                          user=current_user,
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
    
    created_set_tournament = form.set_tournament.data
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
                  total_matches=created_total_matches,
                  tournament=created_set_tournament
                  )
    

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


# Head to Head page to begin querying User head to head. tag1 and tag2 refer to users submitted after the redirect.
@app.route('/head_to_head', methods=['GET', 'POST'])
def head_to_head():
  form = HeadToHead()

  tag1 = request.args.get('tag1')
  tag2 = request.args.get('tag2')
  sets = []
  
  # if tag1 and tag2 are in query string, or basically if user has already submitted data
  if 'tag1' in request.args and 'tag2' in request.args:
    sets = Set.query.filter(and_(Set.winner_tag==tag1, Set.loser_tag==tag2)).all() + Set.query.filter(and_(Set.winner_tag==tag2, Set.loser_tag==tag1)).all()
    sets = sorted(sets, key=lambda x: x.id) # Sort by Set id
    
    #if requesting data, i.e. form may be filled after already viewing a current head to head
    if request.method == 'GET':
      form.user1.data = tag1 # populates the user1 field (in forms.py) with tag1
      form.user2.data = tag2

  if form.validate_on_submit():
    # user1 and user2 is a string that represents the first user's tag
    user1 = form.user1.data
    user2 = form.user2.data

    valid_users = User.query.filter(User.tag==user1).count() + User.query.filter(User.tag==user2).count()

    if valid_users < 2:
      flash('At least one User not found.')
      return redirect(url_for('head_to_head'))
    
    return redirect(url_for('head_to_head', tag1=user1, tag2=user2))

  return render_template("head_to_head.html",
                        title="Head to Head",
                        tag1=tag1,
                        tag2=tag2,
                        setlist=sets,
                        form=form) 


# Compares one user to two others, and will generate two head to heads side by side
@app.route('/compare') #eventually route to this from head_to_head
def compare():
  # Query methods and validation
  
  #sets1 = Set.query.filter(and_(Set.winner_tag==compare_tag, Set.loser_tag==tag1)).all() + Set.query.filter(and_(Set.winner_tag==tag1, Set.loser_tag==compare_tag))
  #sets2 = Set.query.filter(and_(Set.winner_tag==compare_tag, Set.lower_tag==tag1)).all() + Set.query.filter(and_(Set.winner_tag==tag2, Set.loser_tag==compare_tag))
  tag1 = 'hi'
  tag2 = 'lo'
  return head_to_head(tag1, tag2)

@app.route('/browse_sets')
def browse_sets():
  setlist = Set.query.order_by(Set.id).all()
  return render_template("browse_sets.html",
                         title='Browse Sets',
                         setlist=setlist)


@app.route('/browse_users') # browse users
def browse_users():
  userlist = User.query.order_by(User.id).all()
  return render_template("browse_users.html",
                        title='Browse Users',
                        userlist=userlist)


@app.route('/user/<tag>') # User profile page
def user(tag):
  user = User.query.filter(User.tag==tag).first() # If routed to user profile page (user/<tag>), check to make sure user exists
  if user is None:
    flash('User %s not found.' % tag)
    return redirect(url_for('index'))
  
  user_sets = user.getAllSets() # Store all user's sets in variable user_sets
  user_secondaries = user.get_secondaries()
  return render_template("user.html",
                        title=tag,
                        user=user,
                        user_sets=user_sets,
                        user_secondaries=user_secondaries)


# Displays all users given a region. Routed to from /browse_regions
@app.route('/region/<region>')
def region(region):
  matching_users = User.query.filter(User.region==region).order_by(User.id).all() # checks to see if user.region is identical to region
  if matching_users == []:
    flash('No players found in this region') # no user found with matching region
  return render_template("region.html",
                         matching_users=matching_users,
                         region=region)


# Displays all regions currently populated by players. Each displayed region will route to /region/<region>
@app.route('/browse_regions')
def browse_regions():

  userlist = User.query.order_by(User.id).all()
  regionlist = []
  for user in userlist:
    if user.region not in regionlist:
      regionlist += [user.region]

  regionlist.sort()

  return render_template("browse_regions.html", 
                          title='Browse Regions',
                          regionlist=regionlist)




# Displays a list of all SSBM characters, each of which links to /character/<character>
@app.route('/browse_characters')
def browse_characters():
  characterlist = main_char_list

  return render_template("browse_characters.html",
                         characterlist=characterlist)


# Displays all users who play a certain character. Routed to from /browse_characters
@app.route('/character/<character>')
def character(character):
  main_matching_users = User.query.filter(User.main==character).order_by(User.id).all()
  if main_matching_users == []:
    flash('No players found that main this character')
  
  # "Convert" character parameter, which is currently a string, to Character object.
  character_object = Character.query.filter(Character.name==character).first()
  if character_object:
    secondaries_matching_users = character_object.get_users()
  else:
    secondaries_matching_users = []

    if secondaries_matching_users == []:
      flash('No players found that secondary this character')

  return render_template("character.html",
                         main_matching_users=main_matching_users,
                         secondaries_matching_users=secondaries_matching_users,
                         character=character)


#Displays all sets in a given tournament
@app.route('/tournament/<tournament>')
def tournament(tournament):
  tournament_setlist = Set.query.filter(Set.tournament==tournament).order_by(Set.id).all()
  if tournament_setlist == []:
    flash('No sets found for this tournament.')
  
  return render_template("tournament.html",
                         tournament=tournament,
                         tournament_setlist=tournament_setlist)

# During production mode (runp.py), debug is turned OFF and these error templates appear
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
