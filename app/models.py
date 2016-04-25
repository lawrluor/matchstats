from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey, and_, or_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from forms import character_choices, character_list

import sys
sys.path.append('./sanitize')
from sanitize_utils import check_and_sanitize_tag

# the Child to the Parent User in User-Character association
class Character(db.Model):
  __tablename__ = 'character'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True)

  def __repr__(self):
    return '<id: %s, name: %s>' % (self.id, self.name)

  def __str__(self):
    return self.name
  
  def uses_character(self, user):
    return self.users.filter(and_(characters.c.user_id==user.id, characters.c.character_id==self.id)).count() > 0
    

# association table between Character and User
characters = db.Table('characters',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('character_id', db.Integer, db.ForeignKey('character.id'))
                       )

# Child in one-to-many relationship with User
class TrueSkill(db.Model):
  __tablename__ = 'trueskill'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  mu = db.Column(db.Float)
  cons_mu = db.Column(db.Float)
  sigma = db.Column(db.Float)
  region = db.Column(db.String(128))
  rank = db.Column(db.Integer)

  def __repr__(self):
    return '<region: %s, mu: %s, sigma: %s, cons_mu: %s, rank: %s>' % (self.region, self.mu, self.sigma, self.cons_mu, self.rank)


# Region model associated with Users and Tournaments
class Region(db.Model):
  __tablename__ = "region"
  id = db.Column(db.Integer, primary_key=True)
  region = db.Column(db.String(64), index=True, unique=True)
  users = db.relationship("User", order_by="User.id", backref="region")
  tournament_headers = db.relationship("TournamentHeader", order_by="Tournament.date", backref="region")
  tournaments = db.relationship("Tournament", order_by="Tournament.date", backref="region")

  def __repr__(self):
    return '<region: %s, id: %s, users: %s, tournaments: %s>' % (self.region, self.id, len(self.users), len(self.tournaments))

  def __str__(self):
    return self.region

  def adopt_user(self, user_tag):
    user = User.query.filter(User.tag==user_tag).first()
    users.append(user)
    db.session.commit()
    return user

  def adopt_tournament(self, tournament_name):
    tournament = Tournament.query.filter(Tournament.name==tournament_name).first()
    self.tournaments.append(tournament)
    db.session.commit()
    return tournament
    

# the Parent to the Child Character in User-Character association
class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String(128), index=True, unique=True)
  region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
  trueskills = db.relationship("TrueSkill", order_by='TrueSkill.id', backref='user')
  characters = db.relationship("Character",
                              secondary=characters,
                              backref=db.backref("users", lazy="dynamic"),
                              lazy='dynamic')

  def __repr__(self):
    return '<Tag: %s, Region: %s, TrueSkills: %s, characters: %s>' % (unicode(self.tag), self.region, self.trueskills, self.characters.all())
 
  # User-Set Relationship functions
  # get_won_sets is a function that takes a User object and returns the sets he has won.
  def get_won_sets(self):
    sets_won = Set.query.filter(Set.winner_tag==self.tag).order_by(Set.id).all()
    return sets_won

  # get_lost_sets is a function that takes a User object and returns the sets he has lost
  def get_lost_sets(self):
    sets_lost = Set.query.filter(Set.loser_tag==self.tag).order_by(Set.id).all()
    return sets_lost

  # get_all_sets is a function that takes a User object and queries for all Sets he has participated in
  def get_all_sets(self):
    all_sets_sorted = Set.query.filter(or_(Set.winner_id==self.id, Set.loser_id==self.id)).order_by(Set.id).all()     
    return all_sets_sorted

  # Changes User's tag, given string new_tag. Also ensures that user's tag is changed in the Sets he has played
  def change_tag(self, new_tag):
    print "ORIGINAL USER: ", self 
  
    won_sets = self.get_won_sets()
    for set in won_sets:
      set.winner_tag = new_tag
      print set
  
    lost_sets = self.get_lost_sets()
    for set in lost_sets:
      set.loser_tag = new_tag
      print set
    
    self.tag = new_tag
    db.session.commit()
    print "UPDATED USER: ", self
    print self.get_all_sets()

  # User-Character Relationship functions
  # to query "characters" association table, can't use Query. do self.characters.all()  
  # self.characters.all() returns list of Character objects, in __repr__() form
  # What was formerly User.main will refer to User.characters.all()[0], the first Character in list of characters
  def get_characters(self):
    all_characters = self.characters.all()

    processed_characters = []
    for i in range(len(all_characters)):
      char_name = all_characters[i]
      processed_characters.append(char_name)
    return processed_characters # This is a list of strings that represent Character objects
  
  # Takes string representing character object and determines if it is a character Character of a User
  def is_character(self, character):
    char_obj = Character.query.filter(Character.name==character).first()
    if char_obj is None:
      return "Character does not exist"
    else:
      return self.characters.filter(and_(characters.c.user_id==self.id, characters.c.character_id==char_obj.id)).count() > 0

  def add_character(self, character):
    char_obj = Character.query.filter(Character.name==character).first()
    if self.is_character(character):
      return "This Character is already a character of User"
    else:
      self.characters.append(char_obj)
    db.session.commit()
    return self
  
  def remove_character(self, character):
    char_obj = Character.query.filter(Character.name==character).first()
    if self.is_character(character):
      self.characters.remove(char_obj)
    else:
      return "This Character is not a character of User"
    db.session.commit()
    return self 

  def add_characters_list(self, characterlist):
    for i in range(len(characterlist)):
      character = Character.query.filter(Character.name==characterlist[i]).first()
      if characterlist[i] in character_list: # character_list is static list from app/forms.py
        if not self.is_character(character.name):
          self.add_character(character.name)
        else:
          print "Character %s is already a character of User" % character.name
    db.session.commit()
    return self

  def remove_characters_list(self, characterlist):
    for i in range(len(characterlist)):
      character = Character.query.filter(Character.name==characterlist[i]).first()
      if characterlist[i] in character_list: # character_list is static list from app/forms.py
        if self.is_character(character.name):
          self.remove_character(character.name)
        else:
          print "Character %s is not a character of User" % character.name
    db.session.commit()
    return self

  # Returns the first Character in self.characters, list of User's Characters.
  # self.characters.all()[0] refers to the character User.main used to
  def get_main(self):
    if len(self.characters.all()) > 0:
      return self.characters.all()[0]
    else:
      return "No Character found"


# Based on tag parameter, queries User database to locate the respective User; if not found, creates new one, and adds to the database; in either case User is returned. If region parameter is provided, adds region after User creation.
# If first time the User is encountered (i.e. created during this function, it will create a User with the respective region field. Region is primarily provided by parse_challonge_standings
def check_set_user(set_user_tag, *args):
  # Get optional Region object argument, if provided
  if len(args)==1:
    if args[0] is not None:
      if type(args[0])==str:
        user_region = args[0]
      else:
        user_region = args[0].region
    else:
      user_region = None
  else:
    user_region = None

  # When Challonge player uses an account icon, a '\n' character is produced. Check for this by stripping it off the end
  sanitized_tag = check_and_sanitize_tag(set_user_tag, user_region)
  set_user = User.query.filter(User.tag==sanitized_tag).first()
  if set_user is None:
    # Create new user, initializing tag (User.id automatically assigned)
    # if tag over 64 characters, truncated
    set_user = User(tag=sanitized_tag[:64])
    found_region = Region.query.filter(Region.region==user_region).first()
    set_user.region = found_region 

    db.session.add(set_user)
    db.session.commit()
  return set_user


#association object between Tournament and User
class Placement(db.Model):
  __tablename__ = 'placement'
  tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'),  primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
  placement = db.Column(db.Integer)
  tournament_name = db.Column(db.String(256))
  seed = db.Column(db.Integer)
  user = db.relationship("User", backref=backref("tournament_assocs", cascade='all, delete-orphan'))
  tournament = db.relationship("Tournament", backref=backref("placements", cascade='all, delete-orphan'))

  def __repr__(self):
    return '<tournament_id: %s, tournament_name: %s, user_id: %s, seed: %s, placement: %s, user: %s>' % (self.tournament_id, self.tournament_name, self.user_id, self.seed, self.placement, self.user)

  def __unicode__(self):
   return unicode(self.placement) + ": " + unicode(self.seed) + ', ' + unicode(self.user)

# Header for Tournament, mainly including info, non-game related info, and containing the brackets in a multi-stage tournament
# Parent of Tournament in one to many relationship
class TournamentHeader(db.Model):
  __tablename__ = 'tournament_header'
  id = db.Column(db.Integer, primary_key=True)
  official_title = db.Column(db.String(256), index=True)
  host = db.Column(db.String(128), index=True)
  url = db.Column(db.String(256), index=True)
  public_url = db.Column(db.String(256), index=True)
  entrants = db.Column(db.Integer)
  game_type = db.Column(db.String(128), index=True)
  date = db.Column(db.Date)
  name = db.Column(db.String(256), index=True)
  region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
  sub_tournaments = db.relationship("Tournament", backref="header")

  def __repr__(self):
    return '<TournamentHeader: %s, region: %s, title: %s, host: %s, url: %s, entrants: %s, game_type: %s, date: %s, name: %s, sub_tournaments: %s' \
    % (self.name, self.region, self.official_title, self.host, self.url, self.entrants, self.game_type, self.date, self.name, self.sub_tournaments)

  # Get overall entrants for tournamentHeader by adding entrants in sub_tournaments excluding those in final bracket (last bracket in tournament_header.sub_tournaments)
  # Only accurate if all players entered pools (weren't pre-seeded in final bracket)
  def get_final_entrants(self):
    cumulative_entrants = 0
    sub_tournaments = self.sub_tournaments
    if len(sub_tournaments) > 1:
      for i in range(len(sub_tournaments) - 1):
        cumulative_entrants += sub_tournaments[i].entrants
    else:
      cumulative_entrants = sub_tournaments[0].entrants
    self.entrants = cumulative_entrants
    db.session.commit()
    return self.entrants


# Tournament is the many in a one-to-many relationship with model Set
class Tournament(db.Model):
  __tablename__ = 'tournament'
  id = db.Column(db.Integer, primary_key=True)
  parent_id = db.Column(db.Integer, db.ForeignKey('tournament_header.id'))
  official_title =  db.Column(db.String(256), index=True)
  host = db.Column(db.String(128), index=True)
  url = db.Column(db.String(256), index=True)
  public_url = db.Column(db.String(256), index=True)
  entrants = db.Column(db.Integer)
  bracket_type = db.Column(db.String(128), index=True)
  game_type = db.Column(db.String(128), index=True)
  date = db.Column(db.Date)
  name = db.Column(db.String(256), index=True)
  region_id = db.Column(db.Integer, db.ForeignKey('region.id'))
  sets = db.relationship("Set", backref="tournament")

  def __repr__(self):
    return '<tournament: %s, region: %s, title: %s, host: %s, url: %s, public_url: %s, entrants: %s, bracket_type: %s, game_type: %s, date: %s, name: %s, sets: %s>' \
    % (self.name, self.region, self.official_title, self.host, self.url, self.public_url, self.entrants, self.bracket_type, self.game_type, self.date, self.name, len(self.sets))


# Set is the one in a one-to-many relationship with model Match
class Set(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  winner_id = db.Column(db.Integer)
  loser_id = db.Column(db.Integer)
  winner_tag = db.Column(db.String(64), index=True)
  loser_tag = db.Column(db.String(64), index=True)
  winner_score = db.Column(db.Integer)
  loser_score = db.Column(db.Integer)
  max_match_count = db.Column(db.Integer)
  total_matches = db.Column(db.Integer)
  matches = db.relationship('Match', backref="Set", lazy='dynamic')
  round_type = db.Column(db.Integer)
  tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
  tournament_name = db.Column(db.String(256))
  
  def __repr__(self):
    return '<tournament: %s, round %s | winner_tag %s ; winner_id %s: winner_score %s | loser_tag %s ; loser_id %s: loser_score %s>' % (self.tournament_name, self.round_type, self.winner_tag, self.winner_id, self.winner_score, self.loser_tag, self.loser_id, self.loser_score)
  
  def __unicode__(self): # String representation to be printed in html. Ex: Armada vs Mango: (3-2) Armada
    return self.tournament_name.encode('utf-8', 'ignore') + ', Round: ' + unicode(self.round_type) + ' | ' + self.winner_tag.encode('utf-8', 'ignore') + '_' + unicode(self.winner_id) + ' vs ' + self.loser_tag.encode('utf-8', 'ignore') + '_' + unicode(self.loser_id) + ': (' + unicode(self.winner_score) + '-' + unicode(self.loser_score) + ') ' + self.winner_tag.encode('utf-8', 'ignore')
  
  # returns winner (user) of this set
  def getSetWinner(self):
    set_winner = User.query.filter(User.tag==self.winner_tag).first() 
    return set_winner # return winner_tag of the set, the User who won the set
  
  # returns winner ID (user.id) of a Set object
  def getSetWinnerID(self):
    set_winner = self.getSetWinner()
    return set_winner.id

  # returns loser ID (user.id) of a Set object
  def getSetLoserID(self):
    set_loser = self.getSetLoser()
    return set_loser.id

  # returns loser (user) of associated set
  def getSetLoser(self):
    set_loser = User.query.filter(User.tag==self.loser_tag).first()
    return set_loser
  
  # returns True if Set has invalid, impossible score counts for Set
  def invalidScores(self):
    if (winner_score==1 and loser_score==0) or (winner_score==0 and loser_score==-1):
      return False
    else:
      # if standard integers, run calculations to check that scores are valid
      if ((self.winner_score <= self.loser_score) or 
    ((self.winner_score > ((self.max_match_count / 2.0) + 1)) or 
    (self.winner_score < (self.max_match_count / 2.0)))):
        return True 


# Match is the many in a one-to-many relationship with model Set
class Match(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  set_id = db.Column(db.Integer, db.ForeignKey('set.id')) # relationship to Set
  stage = db.Column(db.String(128), index=True) # later map dictionary with stages?
  winner = db.Column(db.String(128), index=True)
  loser = db.Column(db.String(128), index=True)
  winner_char = db.Column(db.String(128), index=True)
  loser_char = db.Column(db.String(128), index=True)

  def __repr__(self):
    return '<Stage: %r, Winner: %r (%r), Loser: %r (%r)>' % (self.stage, self.winner, self.winner_char, self.loser, self.loser_char)

  def __unicode__(self): # String representation to be printed in html. Ex: Stage: Battlefield | Winner: Mango | Loser: Armada
    string_Match = 'Stage: ' + self.stage + ' | Winner: ' + self.winner + ' (' + unicode(self.winner_char) + ') | Loser: ' + self.loser + ' (' + unicode(self.loser_char) + ')'
    return string_Match


