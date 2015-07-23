from app import db # imports database object from __init__.py
from sqlalchemy import Table, Column, Integer, ForeignKey, and_, or_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from forms import main_char_choices, secondaries_char_choices, main_char_list, secondaries_char_list

# the Child to the Parent User in User-Character association
class Character(db.Model):
  __tablename__ = 'character'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True)

  def __repr__(self):
    return '<id: %s, name: %s>' % (self.id, self.name)
  
  # for incorporation into other features, simply displays Character name
  def __unicode__(self):
    return self.name
  
  # Uses users backref to query for Users
  def get_users(self):
    return self.users.all()

  def uses_secondary(self, user):
    return self.users.filter(and_(secondaries.c.user_id==user.id, secondaries.c.character_id==self.id)).count() > 0
    

# association table between Character and User
secondaries = db.Table('secondaries',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('character_id', db.Integer, db.ForeignKey('character.id'))
                       )

# one to one relationship with User
class TrueSkill(db.Model):
  __tablename__ = 'trueskill'
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  mu = db.Column(db.Float)
  sigma = db.Column(db.Float)

  def __repr__(self):
    return '<mu: %s, sigma: %s>' % (self.mu, self.sigma)
  
# Region model associated with Users and Tournaments
class Region(db.Model):
  __tablename__ = "region"
  id = db.Column(db.Integer, primary_key=True)
  region = db.Column(db.String(64), index=True, unique=True)
  users = db.relationship("User", backref="region")
  tournaments = db.relationship("Tournament", backref="region")

  def __repr__(self):
    return '<region: %s, id: %s, users: %s, tournaments: %s>' % (self.region, self.id, self.users, self.tournaments)

  def __str__(self):
    return self.region

# the Parent to the Child Character in User-Character association
class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String(64), index=True, unique=True)
  main = db.Column(db.String(64), index=True)
  region_name = db.Column(db.String(64), ForeignKey('region.id'))
  trueskill = db.relationship("TrueSkill", uselist=False, backref="user")
  secondaries = db.relationship("Character",
                              secondary=secondaries,
                              backref=db.backref("users", lazy="dynamic"),
                              lazy='dynamic')

  def __repr__(self):
    return '<Tag: %s, trueskill: %s, Region: %s, Main: %s, Secondaries: %s>' % (unicode(self.tag), self.trueskill, self.region, self.main, unicode(self.secondaries.all()))
 
  def __unicode__(self):
    return unicode(self.tag) + ' | Region: ' + unicode(self.region) + ' | Main: ' + unicode(self.main) + ' | Secondaries: ' + unicode(self.secondaries.all())

  # User-Set Relationship functions
  # getWonSets is a function that takes a user and returns the sets he has won.
  def getWonSets(self):
    sets_won = Set.query.filter(Set.winner_tag==self.tag).order_by(Set.id).all()
    return sets_won

  # getLostSets is a function that takes a user and returns the sets he has lost
  def getLostSets(self):
    sets_lost = Set.query.filter(Set.loser_tag==self.tag).order_by(Set.id).all()
    return sets_lost

  # getAllSets is a function that takes two lists, sets_won and sets_lost, and sorts them by set id
  def getAllSets(self, sets_won, sets_lost):
    all_sets = sets_won + sets_lost 
    all_sets_sorted = sorted(all_sets, key=lambda x: x.id)
    # code for getting all sets explicitly with query, without helper methods getLostSets and getWonSets
    # sets_test = Set.query.filter(or_(Set.winner_id==user.id, Set.loser_id==user.id)).order_by(Set.id).all()
    return all_sets_sorted

  # User-Character Relationship functions
  # to query "secondaries" association table, can't use Query. do self.secondaries.all()  
  # self.secondaries.all() returns list of Character objects, in __repr__() form
  def get_secondaries(self):
    all_secondaries = self.secondaries.all()
    
    # all_secondaries is list.. yet not iterable?
    # secondaries.name yields 'list' object has no attribute 'name'

    processed_secondaries = []
    for i in range(len(all_secondaries)):
      char_name = unicode(all_secondaries[i])
      processed_secondaries.append(char_name)

    return processed_secondaries # This is a list of strings that represent Character objects

  def is_secondary(self, character):
    return self.secondaries.filter(and_(secondaries.c.user_id == self.id, secondaries.c.character_id == character.id)).count() > 0

  def add_secondaries(self, character):
    if not self.is_secondary(character):
      self.secondaries.append(character)
      return self
  
  def remove_secondaries(self, character):
    if self.is_secondary(character):
      self.secondaries.remove(character)
      return self

  def add_secondaries_list(self, characterlist):
    for i in range(len(characterlist)):
      if characterlist[i] in secondaries_char_list and characterlist[i] != self.main:
        character = Character.query.filter(Character.name == characterlist[i]).first()
        self.add_secondaries(character)
    return self

  def remove_secondaries_list(self, characterlist):
    for i in range(len(characterlist)):
      if characterlist[i] in secondaries_char_list and characterlist[i] != self.main:
        character = Character.query.filter(Character.name == characterlist[i]).first()
        self.remove_secondaries(character)
    return self
   

# Based on tag parameter, queries User database to locate the respective User; if not found, creates new one, and adds to the database; in either case User is returned.
def check_set_user(set_user_tag):
  set_user  = User.query.filter(User.tag==set_user_tag).first()
  if set_user is None:
    # Create new user, initializing tag (User.id automatically assigned)
    set_user = User(tag=set_user_tag)
    db.session.add(set_user) 
    db.session.commit()
  return set_user

# transfers the data the User represented by joined_tag has to User root_tag, while deleting the User represented by joined_tag
# currently doesn't actually link the Users or tag in any way before deletion
# currently doesn't change Matches
def make_same_user(root_tag, joined_tag):
  root_user = User.query.filter(User.tag==root_tag).first()
  print root_user
  joined_user = User.query.filter(User.tag==joined_tag).first()
  print joined_user
  # transfer Set data by simply editing Sets to have the root_user as the winner/loser tag and id
  joined_sets = joined_user.getAllSets()
  for set in joined_sets:
    if set.winner_tag==joined_user.tag:
      set.winner_tag = root_user.tag
      set.winner_id = root_user.id
    else:
      set.loser_tag = root_user.tag
      set.loser_id = root_user.id

  db.session.delete(joined_user) 
  db.session.commit()
  return root_user

# given user tag, returns a simple dictionary with keys tournament_name and value placement for a tournament a User has attended
def get_tournament_name_and_placing(user_tag):
  user = User.query.filter(User.tag==user_tag).first()
  user_placements = {}

  for tournament_placement in user.tournament_assocs:
    tournament_name = tournament_placement.tournament.name
    placement  = convert_placement(tournament_placement.placement)
    user_placements[tournament_name] = placement

  print user_placements
  return user_placements


#association object between Tournament and User
class Placement(db.Model):
  __tablename__ = 'placement'
  tournament_id = db.Column(db.Integer, ForeignKey('tournament.id'), primary_key=True)
  user_id = db.Column(db.Integer, ForeignKey('user.id'), primary_key=True)
  placement = db.Column(db.Integer)
  tournament_name = db.Column(db.String(128))
  seed = db.Column(db.Integer)
  user = db.relationship("User", backref=backref("tournament_assocs", cascade='all, delete-orphan'))

  def __repr__(self):
    return '<tournament_id: %s, tournament_name: %s, user_id: %s, seed: %s, placement: %s, user: %s>' % (self.tournament_id, self.tournament_name, self.user_id, self.seed, self.placement, self.user)

  def __unicode__(self):
   return unicode(self.placement) + ": " + unicode(self.seed) + ', ' + unicode(self.user)

# Tournament is the many in a one=to-many relationship with model Set
class Tournament(db.Model):
  __tablename__ = 'tournament'
  id = db.Column(db.Integer, primary_key=True)
  official_title =  db.Column(db.String(128), index=True)
  host = db.Column(db.String(128), index=True)
  entrants = db.Column(db.Integer)
  bracket_type = db.Column(db.String(128), index=True)
  game_type = db.Column(db.String(128), index=True)
  date = db.Column(db.Date)
  name = db.Column(db.String(128), index=True)
  tournament_type = db.Column(db.String(64), index=True)
  region_name = db.Column(db.String(64), ForeignKey('region.id'))
  sets = db.relationship("Set", backref="tournament") 
  # users is a list of Placement objects
  users = db.relationship("Placement", backref="tournament")

  def __repr__(self):
    return '<tournament: %s, tournament_type: %s, region: %s, title: %s, host: %s, entrants: %s, bracket_type: %s, game_type: %s, date: %s, name: %s, sets: %s, users: %s>' % (self.name, self.tournament_type, self.region, self.official_title, self.host, self.entrants, self.bracket_type, self.game_type, self.date, self.name, self.sets, self.users)

# given Tournament object, if tournament name already exists, if tournament is a pool of a larger one, add placements and sets to Tournament object and return it, else simply return original Tournament object
def check_tournament(tournament):
  same_tournament = Tournament.query.filter(Tournament.name==tournament.name).first()
  # if tournament already exists, only add matches to Tournament, else create tournament as usual
  if same_tournament is not None:
    # if tournament.type == "Pool"
    same_tournament.sets.append(tournament.sets) 
  else:
    print "Tournament already exists" 
  return same_tournament


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
  tournament_id = db.Column(db.Integer, ForeignKey('tournament.id'))
  tournament_name = db.Column(db.String(128))
  
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


