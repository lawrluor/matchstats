# Version 2.0 routes commented out, consisting primarily of user creating/editing model objects
from flask import render_template, flash, redirect, request, url_for, g, session
from app import app, db
from models import User, Set, Match, Character, Placement, secondaries, Region
from forms import UserCreate, UserEdit, SetCreate, SetEdit, MatchSubmit, HeadToHead, SearchForm, CharacterFilter, main_char_choices, secondaries_char_choices, main_char_list, secondaries_char_list, RegionSelect
from sqlalchemy import and_, or_
from h2h_stats_functions import *
from config import USERS_PER_PAGE, TOURNAMENTS_PER_PAGE, CHAR_USERS_PER_PAGE 

import sys
sys.path.append('./sanitize')
from sanitize_utils import check_and_sanitize_tag, check_and_sanitize_tag_multiple
from sort_utils import sort_placementlist, sort_userlist
from h2h_stats_functions import convert_placement
import collections

"""
This module includes all routing functions for this web application.

Look at basic flask tutorials but the general pattern is:
@app.route('/$SOME_ROUTE', methods=['GET','POST'])
def $ROUTE_NAME($OPTIONAL_PARAMS):
  ...
  return render_template("$HTML_FILENAME", $OPTIONAL_VALUES)
"""

# Registers a function to run before each request. g.search_form makes form global so the field's data can be accessed from anywhere
@app.before_request
def before_request():
  g.search_form = SearchForm()
  
  # get region_name
  if 'region_name' in session:
    g.region = session['region_name']
  else:
    g.region = "Global" 

  # populate RegionSelect form with name of current Region
  g.region_form = RegionSelect(region_name=g.region)

# Region select route, to process RegionSelect form data
@app.route('/select_region', methods=['POST'])
def select_region():
  form = RegionSelect() 
  session['region_name'] = form.region_name.data

  # Global and National are not actual Region name, but acts as a string identifier for when no Region is selected
  if session['region_name']=="Global":
    flash("Viewing Global Information - this view mode displays all information from every region") 
    return redirect(url_for('home'))
  elif session['region_name']=="National":
    flash("Viewing National Information - this view mode only displays non-regional tournament information") 
    return redirect(url_for('home'))
  else:
    return redirect(url_for('region', region=session['region_name']))

# Home page
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
  flash('Help out SmashStats and your region! If you notice incorrect or missing information, please let us know via social media!')

  # Display recently added tournaments
  tournamentlist = Tournament.query.order_by(Tournament.id.desc()).limit(10).all()
  for tournament in tournamentlist:
    print tournament
  return render_template('home.html',
                         tournamentlist=tournamentlist)

# About page (more info)
@app.route('/about')
def about():
  return render_template('about.html')

# Head to Head page to begin querying User head to head. tag1 and tag2 refer to users submitted after the redirect.
@app.route('/head_to_head', methods=['GET', 'POST'])
def head_to_head():
  form = HeadToHead()
  
  # if query string arguments exist (form submitted), create these variables using query string
  tag1 = request.args.get('tag1')
  tag2 = request.args.get('tag2')
  user1 = request.args.get('user1')
  user2 = request.args.get('user2')
  user1_set_win_count = request.args.get('user1_set_win_count')
  user2_set_win_count = request.args.get('user2_set_win_count')
  user1_match_win_count = request.args.get('user1_match_win_count')
  user2_match_win_count = request.args.get('user2_match_win_count')
  user1_score_matches_won = request.args.get('user1_score_matches_won')
  user2_score_matches_won = request.args.get('user2_score_matches_won')
  h2h_sets_played = request.args.get('h2h_sets_played')
  h2h_matches_played = request.args.get('h2h_matches_played')
  h2h_stages_played = request.args.get('h2h_stages_played')
  mutual_tournaments = request.args.get('mutual_tournaments')

  # to be displayed when tag1 and tag2 are valid Users, but needs to be initialized here so the pre_submit template doesn't crash 
  all_sets = []
  all_matches = 0
  
  # if tag1 and tag2 are in query string, or basically if user has already submitted data
  if 'tag1' in request.args and 'tag2' in request.args:
    # given sanitized tags, query for User objects
    user1 = User.query.filter(User.tag==tag1).first()
    user2 = User.query.filter(User.tag==tag2).first()

    h2h_sets_played = h2h_get_sets_played(user1, user2)
    user1_set_win_count = len(h2h_get_sets_won(user1, user2))
    user2_set_win_count = len(h2h_get_sets_won(user2, user1))

    # before moving forward, calculate matches by iterating through sets 
    h2h_matches_played = h2h_get_matches_played(h2h_sets_played) 
    user1_matches_won = h2h_get_matches_won(user1, user2, h2h_matches_played)
    user2_matches_won = h2h_get_matches_won(user2, user1, h2h_matches_played)
    user1_match_win_count = len(user1_matches_won)
    user2_match_win_count = len(user2_matches_won)
    # calculate stage statistics
    h2h_stages_played = h2h_get_stages_played(h2h_matches_played)

    # for Set with no Match objects available, look into Set scores to determine match wins and losses
    user1_score_matches_won = 0
    user2_score_matches_won = 0
    for set in h2h_sets_played:
      if set.winner_tag == tag1:
        user1_score_matches_won += set.winner_score
        user2_score_matches_won += set.loser_score
      else:
        user2_score_matches_won += set.winner_score
        user1_score_matches_won += set.loser_score

    # query Tournaments to find Tournaments both users have attended
    mutual_tournaments = h2h_get_mutual_tournaments(user1, user2)

    # if requesting data, i.e. form may be filled after already viewing a current head to head
    if request.method == 'GET':
      form.user1.data = tag1 # populates the user1 field (in forms.py) with tag1
      form.user2.data = tag2

  if form.validate_on_submit():
    # user1 and user2 is a string that represents the first user's tag
    user1_tag = check_and_sanitize_tag(form.user1.data)
    user2_tag = check_and_sanitize_tag(form.user2.data)

    # Make sure two Users are found, else redirect to pre-validated form
    user1 = User.query.filter(User.tag==user1_tag).first()
    user2 = User.query.filter(User.tag==user2_tag).first()
    if user1 is None or user2 is None:
      flash("At least one player not found.")
      return redirect(url_for('head_to_head'))
    else:
      return redirect(url_for('head_to_head', tag1=user1.tag, tag2=user2.tag))

  return render_template("head_to_head.html",
                        title="Head to Head",
                        tag1=tag1,
                        tag2=tag2,
                        user1=user1,
                        user2=user2,
                        user1_set_win_count=user1_set_win_count,
                        user2_set_win_count=user2_set_win_count,
                        user1_match_win_count=user1_match_win_count,
                        user2_match_win_count=user2_match_win_count,
                        user1_score_matches_won=user1_score_matches_won,
                        user2_score_matches_won=user2_score_matches_won,
                        h2h_sets_played=h2h_sets_played,
                        h2h_matches_played=h2h_matches_played,
                        h2h_stages_played=h2h_stages_played,
                        mutual_tournaments=mutual_tournaments,
                        form=form) 


# browse all Users, 25 per page
@app.route('/browse_users')
@app.route('/browse_users/<int:page>')
def browse_users(page=1):
  # if viewing global information, don't filter query by g.region
  # if character=="Main", or the default SelectField "title", don't filter for any character
  if g.region=="Global" or g.region=="National":
    userlist = User.query.join(TrueSkill.user, User).filter(TrueSkill.region=="Global").order_by(TrueSkill.cons_mu.desc()).paginate(page, USERS_PER_PAGE, False)
  else:
    # filter by g.region by joining Region and User.region, and order by Trueskill by joining Trueskill and User.trueskill
    userlist = User.query.join(TrueSkill.user, User).filter(TrueSkill.region==g.region).order_by(TrueSkill.cons_mu.desc()).paginate(page, USERS_PER_PAGE, False)
  return render_template("browse_users.html",
                         userlist=userlist,
                         current_region=g.region
                         )

# User profile page
@app.route('/user/<tag>')
@app.route('/user/<tag>/<int:page>')
def user(tag, page=1):
  # Pagination variables
  tournaments_per_page = 10 
  start_index = (page - 1) * tournaments_per_page
  end_index = start_index + tournaments_per_page

  user = User.query.filter(User.tag==tag).first()
  # If routed to user profile page (user/<tag>), check to make sure user exists
  if user is None:
    flash('User %s not found.' % tag)
    return redirect(url_for('browse_users'))

  # get User secondaries
  user_secondaries = user.get_secondaries()
  
  # create ordered dictionary with Tournament name and respective placement; important to keep order so placements can be displayed in order of tournament.date 
  user_placements = collections.OrderedDict()
  user_sets_by_tournament = collections.OrderedDict()

  # sort by Placement.tournament.date, in reverse order (most recent first). Sort by tournament.name as secondary sort
  user_tournaments_sorted = sort_placementlist(user.tournament_assocs) 
  for placement_obj in user_tournaments_sorted[start_index:end_index]:
    # Make dictionary of lists with key tournament_name, and list[0]=placement, list[1]=seed
    tournament_name = placement_obj.tournament.name
    placement  = convert_placement(placement_obj.placement)
    user_placements[tournament_name] = [placement, placement_obj.seed]

    user_tournament_sets = Set.query.filter(and_(Set.tournament_name==tournament_name, or_(Set.winner_tag==user.tag, Set.loser_tag==user.tag))).order_by(Set.id).all()
    for set in user_tournament_sets:
      key = user_sets_by_tournament.setdefault(tournament_name, [])
      key.append(set)

  # get number of Sets won and lost as integers to pass to template
  user_set_wins = len(user.get_won_sets())
  user_set_losses = len(user.get_lost_sets())

  return render_template("user.html",
                        user=user,
                        user_set_wins=user_set_wins,
                        user_set_losses=user_set_losses,
                        user_secondaries=user_secondaries,
                        user_tournaments_sorted=user_tournaments_sorted,
                        user_placements=user_placements,
                        user_sets_by_tournament=user_sets_by_tournament,
                        page=page,
                        tournaments_per_page=tournaments_per_page)


# Displays all users given a region. Routed to from /browse_regions
@app.route('/region/<region>')
def region(region):
  flash('Help out SmashStats and your region! If you notice incorrect or missing information, please let us know via social media!')
  current_region = Region.query.filter(Region.region==region).first()
  session['region_name']=current_region.region
  flash("Now Viewing Region: " + str(session['region_name']))
  return render_template("region.html",
                         region=region,
                         current_region=current_region)
 

# Displays a list of all SSBM characters, each of which links to /character/<character>
@app.route('/browse_characters')
def browse_characters():
  characterlist = main_char_list
  return render_template("browse_characters.html",
                         characterlist=characterlist,
                         current_region=g.region)

 
# Displays all users who play a certain character. Routed to from /browse_characters
@app.route('/character/<character>')
@app.route('/character/<character>/<int:page>')
def character(character, page=1):
  # if viewing Global information, don't filter query by g.region
  if g.region=="Global" or g.region=="National":
    main_matching_users = User.query.join(TrueSkill.user, User).filter(and_(TrueSkill.region=="Global", User.main==character)).order_by(TrueSkill.cons_mu.desc()).paginate(page, CHAR_USERS_PER_PAGE, False)
# if viewing national information, filter query to take Users with User.region==None
  else:
    main_matching_users = User.query.join(TrueSkill.user, User).join(Region, User.region).filter(and_(TrueSkill.region==g.region, User.main==character, Region.region==g.region)).order_by(TrueSkill.cons_mu.desc()).paginate(page, CHAR_USERS_PER_PAGE, False)
  if main_matching_users.total <= 0:
    flash('No players found that main this character')
  
  # "Convert" character parameter, which is currently a string, to Character object.
  character_object = Character.query.filter(Character.name==character).first()

  if character_object is not None and character=="Unknown":
    # if viewing Global information, don't filter query by g.region
    if g.region=="Global" or g.region=="National":
      secondaries_matching_users = User.query.join(TrueSkill.user, User).filter(and_(TrueSkill.region=="Global"), User.secondaries.contains(character_object)).order_by(TrueSkill.cons_mu.desc()).paginate(page, CHAR_USERS_PER_PAGE, False)
    else:
      secondaries_matching_users = User.query.join(TrueSkill.user, User).join(Region, User.region).filter(and_(TrueSkill.region==g.region, User.secondaries.contains(character_object), Region.region==g.region )).order_by(TrueSkill.cons_mu.desc()).paginate(page, CHAR_USERS_PER_PAGE, False)
  else:
    secondaries_matching_users=None
  
  # Flash notice if no players found that secondary the character
  if secondaries_matching_users is None or secondaries_matching_users.total <= 0:
    flash('No players found that secondary this character')

  return render_template("character.html",
                         main_matching_users=main_matching_users,
                         secondaries_matching_users=secondaries_matching_users,
                         character=character,
                         current_region=g.region)
 

# Lists all tournaments, 15 per page
@app.route('/browse_tournaments')
@app.route('/browse_tournaments/<int:page>')
def browse_tournaments(page=1):
  # if viewing Global information, don't filter query by g.region
  if g.region=="Global":
    tournamentlist = Tournament.query.order_by(Tournament.date.desc()).paginate(page, TOURNAMENTS_PER_PAGE, False)
  # if viewing national information, filter query to take Tournaments with region==None
  elif g.region=="National":
    tournamentlist = Tournament.query.filter(Tournament.region==None).order_by(Tournament.date.desc()).paginate(page, TOURNAMENTS_PER_PAGE, False)
  else:
    # filter for Tournaments by g.region, by joining Region and Tournament.region
    tournamentlist = Tournament.query.join(Region, Tournament.region).filter(Region.region==g.region).order_by(Tournament.date.desc()).paginate(page, TOURNAMENTS_PER_PAGE, False)
  return render_template("browse_tournaments.html",
                         tournamentlist=tournamentlist,
                         current_region=g.region)
    
# Displays all sets in a given tournament
@app.route('/tournament/<tournament_name>')
def tournament(tournament_name):
  # get Tournament object given string name
  tournament_obj = Tournament.query.filter(Tournament.name==tournament_name).first()

  # get Sets
  tournament_setlist = tournament_obj.sets
  if tournament_setlist == []:
    flash('No sets found for this tournament.')
  
  # create dictionary object with key = set.round_type, values = setlists
  matches_by_round = collections.OrderedDict()
  for set in tournament_setlist:
    if set.round_type is not None:
      round_num = matches_by_round.setdefault(set.round_type, [])
      round_num.append(set)

  # generates list of Users in order of their placement
  placement_dict = collections.OrderedDict()
  placement_list = Placement.query.filter(Placement.tournament_id==tournament_obj.id).order_by(Placement.placement).all()

  # store into dictionary to pass to template; stores dictionary of lists with list[0]=placement, list[1]=seed
  for placement_obj in placement_list: 
    placing = placement_dict.setdefault(convert_placement(placement_obj.placement), [])
    placing.append([placement_obj.user.tag, placement_obj.seed])

  return render_template("tournament.html",
                         tournament=tournament_obj,
                         placement_dict=placement_dict,
                         matches_by_round=matches_by_round)


@app.route('/search', methods=['POST'])
def search():
  if not g.search_form.validate_on_submit():
    flash('Search failed.')
    return redirect(url_for('home'))
  return redirect(url_for('search_results', query=g.search_form.search.data))


# processes query from /search and returns search results for Users and tournaments (Set.tournament) on this page
@app.route('/search_results/<query>')
def search_results(query):
  sanitized_query_list = check_and_sanitize_tag_multiple(query)
  tournament_results = Tournament.query.filter(Tournament.name==query).all() 

  print sanitized_query_list
  # pass list of User objects as list to display in search results
  user_results = []
  for sanitized_tag in sanitized_query_list:
    user = User.query.filter(User.tag==sanitized_tag).first() 
    if user is not None:
      user_results.append(user)

  return render_template('search_results.html',
                         query=query,
                         tournament_results=tournament_results,
                         user_results=user_results)


# During production mode (runp.py), debug is turned OFF and these error templates appear
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

#  Somewhat OBSOLETE because of the RegionSelect form
# # Displays all regions currently populated by players. Each displayed region will route to /region/<region>
# @app.route('/browse_regions')
# def browse_regions():
#   regionlist = Region.query.all()
#   return render_template("browse_regions.html", 
#                           title='Browse Regions',
#                           regionlist=regionlist)


# # helper function for set_edit, set_create; similar to Set.invalidScores(), returns True if invalid, impossible score counts. must be used instead of Set.invalidScores() because this checks before creating a Set and no Set exists yet.
# def invalidScores(winner_score, loser_score, max_match_count):
#  # if non-standard integers/strings, ignore them; cases for reported W/L without full score, or a DQ score
#  if (winner_score==1 and loser_score==0) or (winner_score==0 and loser_score==-1):
#    return False
#  else:
#    # if standard integers, run calculations to check that scores are valid
#    if ((winner_score <= loser_score) or 
#    ((winner_score > ((max_match_count / 2.0) + 1)) or 
#    (winner_score < (max_match_count / 2.0)))):
#      return True 
#
#
# @app.route('/set_edit/<set_id>', methods=['GET','POST'])
# def set_edit(set_id):
#   # query Set for Set object with same set_id (the Set itself)
#   current_set = Set.query.filter(Set.id==int(set_id)).first()
#   
#   form = SetEdit()
#   
#   if form.validate_on_submit():
#     current_set.max_match_count = form.edit_max_match_count.data
#     current_set.tournament = form.edit_tournament.data
#     
#     # Based on winner and loser tag submitted through form, queries User database to locate the respective Users
#     set_winner = User.query.filter(User.tag==form.edit_winner_tag.data).first()
#     if set_winner is None:
#       # Create new user, initializing tag (User.id automatically assigned)
#       set_winner = User(tag=form.edit_winner_tag.data) 
#       db.session.add(set_winner)
#      
#     set_loser = User.query.filter(User.tag==form.edit_loser_tag.data).first()
#     if set_loser is None:
#       # Create new user, initializing tag (User.id automatically assigned) 
#       set_loser = User(tag=form.edit_loser_tag.data) 
#       db.session.add(set_loser)
#     
#     current_set.winner_tag = set_winner.tag
#     current_set.winner_id = set_winner.id
#     current_set.loser_tag = set_loser.tag
#     current_set.loser_id = set_loser.id
# 
#     # Check to see if set score count is valid for type of set, and winner score>loser score (directly from set_create())
#     if invalidScores(int(form.edit_winner_score.data), int(form.edit_loser_score.data), int(form.edit_max_match_count.data)): 
#       flash("Check to make sure you have entered the appropriate scores for the set score count.")
#       return redirect(url_for('set_edit', set_id=set_id))
#     
#     # implicit else: scores are valid, and store them in appropriate Set attributes
#     current_set.winner_score = int(form.edit_winner_score.data)
#     current_set.loser_score = int(form.edit_loser_score.data)
#     current_set.total_matches = current_set.loser_score + current_set.winner_score
#      
#     db.session.commit()
#     flash('Changes have been saved.') 
# 
#     # if indication to edit Matches
#     if form.edit_match_info.data==True:
#       # if the Set has matches, send to edit Match page with link to Set and count of total_matches; else, redirect to match submit page
#       if current_set.matches.all():
#         return redirect(url_for('match_edit', set_id=set_id, total_matches=current_set.total_matches))
#       else:
#         return redirect(url_for('match_submit', set_id=set_id, total_matches=current_set.total_matches, set_winner_tag=current_set.winner_tag, set_loser_tag=current_set.loser_tag))
#     else:
#       # if no indiciation to edit Matches, then Set editing is done.
#       return redirect(url_for('set_edit', set_id=set_id))
#   else:
#     # if not submitted form, pre-populate them with the set's current (prior to edit) info
#     if current_set.max_match_count==0:
#       form.edit_max_match_count.data = 0
#     else:
#       form.edit_max_match_count.data = current_set.max_match_count
# 
#     form.edit_tournament.data = current_set.tournament
#     form.edit_winner_tag.data = current_set.winner_tag
#     form.edit_loser_tag.data = current_set.loser_tag
#     form.edit_winner_score.data = int(current_set.winner_score)
#     form.edit_loser_score.data = int(current_set.loser_score)
# 
#   return render_template('set_edit.html', 
#                           title = 'Edit Set',
#                           form=form,
#                           set=current_set
#                           )
# 
# # set_id, total_matches, set_winner, set_loser passed through url from route /set_create as query strings automatically because they weren't passed as parameters of match_sbumit or part of the route /match_submit
# @app.route('/match_submit', methods=['GET', 'POST'])
# def match_submit(): 
#   set_id = request.args.get('set_id')
#   total_matches = request.args.get('total_matches')
#   set_winner = request.args.get('set_winner_tag')
#   set_loser = request.args.get('set_loser_tag')
# 
#   form = MatchSubmit() # instantiate object from MatchSubmit() class in app/forms.py
#   form.match_winner.choices = [(set_winner, set_winner), (set_loser, set_loser)]
#   form.match_loser.choices = [(set_loser, set_loser), (set_winner, set_winner)]
# 
#   if form.validate_on_submit():
#     submitted_match_stage = form.match_stage.data
#     submitted_match_winner = form.match_winner.data
#     submitted_match_loser = form.match_loser.data
#     submitted_winner_char = form.winner_char.data
#     submitted_loser_char = form.loser_char.data
# 
# 
#     new_match = Match(stage=submitted_match_stage,
#                       winner=submitted_match_winner,
#                       loser=submitted_match_loser,
#                       winner_char=submitted_winner_char,
#                       loser_char=submitted_loser_char,
#                       set_id=set_id 
#                       )
#     
#     # commit to db
#     db.session.add(new_match)
#     db.session.commit()
#     
#     # code for submitting the next match in the set
#     total_matches = int(total_matches) - 1 # now that one match has been submitted, there is one less match to be submitted out of the total number initially indicated when set was created
#     if total_matches == 0: # base case: if no more matches to submit, redirected home
#       flash('Submission Complete') 
#       return redirect('/index')
#     else:
#       total_matches = str(total_matches) # necessary to convert again for flash message and more importantly as a parameter of function match_submit
#       flash('Match Submission Complete. Submit next Match. Matches left: ' + total_matches)
#       return redirect(url_for('match_submit', set_id=set_id, total_matches=total_matches, set_winner=set_winner, set_loser=set_loser))
# 
#   return render_template('match_submit.html',
#                           title='Submit Match',
#                           form=form)
# 
# @app.route('/match_edit', methods=['GET', 'POST'])
# def match_edit():
#   set_id = request.args.get('set_id')
#   current_set = Set.query.filter(Set.id==set_id).first()
#   return "Unfinished"

# # Compares one user to two others, and will generate two head to heads side by side
# @app.route('/compare') #eventually route to this from head_to_head
# def compare():
#   # Query methods and validation
#   
#   #sets1 = Set.query.filter(and_(Set.winner_tag==compare_tag, Set.loser_tag==tag1)).all() + Set.query.filter(and_(Set.winner_tag==tag1, Set.loser_tag==compare_tag))
#   #sets2 = Set.query.filter(and_(Set.winner_tag==compare_tag, Set.lower_tag==tag1)).all() + Set.query.filter(and_(Set.winner_tag==tag2, Set.loser_tag==compare_tag))
#   tag1 = 'hi'
#   tag2 = 'lo'
#   return head_to_head(tag1, tag2)
# 
# @app.route('/browse_sets')
# def browse_sets():
#   setlist = Set.query.order_by(Set.id).all()
#   return render_template("browse_sets.html",
#                          setlist=setlist)
#
#
# @app.route('/user_create', methods=['GET', 'POST'])
# def user_create():
#   form = UserCreate() # instantiate object from UserCreate() class in app/forms.py
#   if form.validate_on_submit(): # if True, indicates data is valid and can be processed
#     created_tag = form.user_tag.data # stores entered value in variable
#     created_region = form.user_region.data
#     created_main = form.user_main.data
#     created_secondaries = form.user_secondaries.data
# 
#     # create user row, initializing user object
#     new_user = User(tag=created_tag,
#                 main=created_main,
#                 region=created_region
#                 )
# 
#     # commit to db
#     db.session.add(new_user)
#     db.session.commit()
#     flash('User creation successful.')
#     
#     # now add secondaries to User
#     new_user.add_secondaries_list(created_secondaries)
#     db.session.commit()
# 
#     flash('Secondaries added to User.')
#     return redirect('/browse_users')
# 
#   return render_template('user_create.html', # renders template for creating user if called before user enters data
#                         title='Create User',
#                         form=form)

# @app.route('/user_edit/<user>', methods=['GET', 'POST'])
# def user_edit(user):
#   form = UserEdit()
#   current_user = User.query.filter(User.tag==user).first() 
#   current_secondaries = current_user.get_secondaries() 
#   
#   # only display Characters that can be added (not main character or already secondary) and be removed (already secondary)
#   form.add_secondaries.choices = [(x, x) for x in secondaries_char_list if x != current_user.main and x not in current_secondaries] 
#   form.remove_secondaries.choices = [(x, x) for x in current_secondaries] 
# 
#   if form.validate_on_submit():
#     current_user.tag = form.edit_tag.data
#     current_user.region = form.edit_region.data
#     current_user.main = form.edit_main.data
#     add_characterlist = form.add_secondaries.data
#     remove_characterlist = form.remove_secondaries.data
# 
#     current_user.add_secondaries_list(add_characterlist)
#     current_user.remove_secondaries_list(remove_characterlist)
#     
#     db.session.commit()
#     flash('Changes have been saved.')
#     # important that it's the raw data, otherwise redirect will fail if user tag is changed
#     return redirect(url_for('user', tag=form.edit_tag.data))
#   
#   # populate forms prior to rendering template
#   else:
#     form.edit_tag.data = current_user.tag
#     form.edit_region.data = current_user.region
#     form.edit_main.data = current_user.main
# 
#   return render_template('user_edit.html',
#                           user=current_user,
#                           form=form)
# 
# @app.route('/set_create', methods=['GET', 'POST']) # 'POST' allows us to receive POST requests, which will bring in form data entered by the user
# def set_create():
#   form = SetCreate() # instantiate object from SetCreate() class in app/forms.py
#   if form.validate_on_submit(): # if True, indicates data is valid and can be processed
#     
#     set_winner_tag = form.set_winner_tag.data
#     set_loser_tag = form.set_loser_tag.data
# 
#     # Based on winner and loser tag submitted through form, queries User database to locate the respective Users
#     set_winner = User.query.filter(User.tag==set_winner_tag).first()
#     if set_winner is None:
#       # Create new user, initializing tag (User.id automatically assigned)
#       set_winner = User(tag=form.set_winner_tag.data) 
#       set_winner_id = set_winner.id
#       db.session.add(set_winner)
#     else:
#       set_winner_id = set_winner.id
#      
#     set_loser = User.query.filter(User.tag==set_loser_tag).first()
#     if set_loser is None:
#       # Create new user, initializing tag (User.id automatically assigned) 
#       set_loser = User(tag=form.set_loser_tag.data) 
#       set_loser_id = set_loser.id
#       db.session.add(set_loser)
#     else:
#       set_loser_id = set_loser.id
# 
#     # process the input for winner score and loser score, and "convert" to integers if possible
#     if form.set_winner_score.data=='W' or form.set_loser_score.data=='L':
#       # special 'W' and 'L' scores converted to a 1-0 set; if either is character, render set a 1-0
#       created_set_winner_score = 1
#       created_set_loser_score = 0
#     else:
#       created_set_winner_score = int(form.set_winner_score.data)
#       created_set_loser_score = int(form.set_loser_score.data)
# 
#     # Calculate created_total_matches, total matches in the Set
#     if (created_set_winner_score==0 and created_set_loser_score==-1):
#       created_total_matches = 0 
#     else:
#       created_total_matches = created_set_winner_score + created_set_loser_score
# 
#     # Check tournament name; if None, default is "Non-Tourney"
#     if form.set_tournament.data:
#       created_set_tournament = form.set_tournament.data
#     else:
#       created_set_tournament = "Non-Tourney"
# 
#     created_max_match_count = int(form.set_max_match_count.data)
#    
#     # Check to see if set score count is valid for type of set, and winner score>loser score
#     if invalidScores(created_set_winner_score, created_set_loser_score, created_max_match_count):   
#       flash("Check to make sure you have entered the appropriate scores for the set score count.")
#       return redirect(url_for('set_create'))
# 
#     # create set row, initializing set object
#     new_set = Set(winner_tag=set_winner_tag,
#                   loser_tag=set_loser_tag,
#                   winner_id=set_winner_id,
#                   loser_id=set_loser_id,
#                   winner_score=created_set_winner_score,
#                   loser_score=created_set_loser_score,
#                   max_match_count=created_max_match_count,
#                   total_matches=created_total_matches,
#                   tournament=created_set_tournament
#                   )
#     
#     # commit to db
#     db.session.add(new_set)
#     db.session.commit()
# 
#     if new_set.total_matches <= 0:
#       # if no recorded matches in set, create Set and redirect to /browse_sets
#       flash("Set submitted.")
#       return redirect(url_for('browse_sets'))
#     elif form.no_match_info.data == True:
#       flash("Set submitted.")
#       return redirect(url_for('browse_sets'))
#     else:
#       flash('Next, enter data for the individual matches.') # if Set is created successfully, redirect to the match_create page, where data for individual matches entered
#       return redirect(url_for('match_submit', set_id=str(new_set.id), total_matches=int(new_set.total_matches), set_winner_tag=set_winner_tag, set_loser_tag=set_loser_tag))
# 
#   return render_template('set_create.html', # renders template for creating user if called before user enters data
#                         title='Create Set', 
#                         form=form
#                         )
