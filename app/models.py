from app import db # imports database object from __init__.py
from sqlalchemy import Table, Column, Integer, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# the Child to the Parent User in User-Character association
class Character(db.Model):
  __tablename__ = 'character'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True)

  def __repr__(self):
    return '<id: %s, name: %s>' % (self.id, self.name)

  def __str__(self):
    return 'id: ' + str(self.id) + ', name: ' + self.name
  
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


# the Parent to the Child Character in User-Character association
class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String(64), index=True, unique=True)
  main = db.Column(db.String(64), index=True)
  region = db.Column(db.String(128), index=True) # because db.String(128), need to cast this as a str when using it
  secondaries = db.relationship("Character",
                              secondary=secondaries,
                              backref=db.backref("users", lazy="dynamic"),
                              lazy='dynamic')

  def __repr__(self):
    return '<User %s, Region %s, Main %s, Secondaries %s>' % (self.tag, self.region, self.main, str(self.secondaries.all()))
  
  def __str__(self):
    return self.tag + ' | Region: ' + str(self.region) + ' | Main: ' + self.main + ' | Secondaries: ' + str(self.secondaries.all())
  

  # User-Set Relationship functions
  # getWonSets is a function that takes a user and returns the sets he has won.
  def getWonSets(self):
    sets_won = Set.query.filter(Set.winner_tag==self.tag).order_by(Set.id).all()
    return sets_won

  # getLostSets is a function that takes a user and returns the sets he has lost
  def getLostSets(self):
    sets_lost = Set.query.filter(Set.loser_tag==self.tag).order_by(Set.id).all()
    return sets_lost

  # getAllSets is a function that takes a user and returns all the sets he has played
  def getAllSets(self):
    all_sets = self.getWonSets() + self.getLostSets()
    all_sets_sorted = sorted(all_sets, key=lambda x: x.id)
    return all_sets_sorted


  # User-Character Relationship functions
  # to query "secondaries" association table, can't use Query. do self.secondaries.all()  
  def get_secondaries(self):
    return self.secondaries.all()
  
  def add_secondaries(self, character):
    if not self.is_secondary(character):
      self.secondaries.append(character)
      return self
  
  def remove_secondaries(self, character):
    if self.is_secondary(character):
      self.secondaries.remove(character)
      return self

  def is_secondary(self, character):
    return self.secondaries.filter(and_(secondaries.c.user_id == self.id, secondaries.c.character_id == character.id)).count() > 0


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
  
  def __repr__(self):
    return '<winner_tag %s ; winner_id %s: winner_score %s | loser_tag %s ; loser_id %s: loser_score %s>' % (self.winner_tag, self.winner_id, self.winner_score, self.loser_tag, self.loser_id, self.loser_score)
  
  def __str__(self): # String representation to be printed in html. Ex: Armada vs Mango: (3-2) Armada
    return self.winner_tag + '_' + str(self.winner_id) + ' vs ' + self.loser_tag + '_' + str(self.loser_id) + ': (' + str(self.winner_score) + '-' + str(self.loser_score) + ') ' + self.winner_tag
  
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

  def __str__(self): # String representation to be printed in html. Ex: Stage: Battlefield | Winner: Mango | Loser: Armada
    string_Match = 'Stage: ' + self.stage + ' | Winner: ' + self.winner + ' (' + str(self.winner_char) + ') | Loser: ' + self.loser + ' (' + str(self.loser_char) + ')'
    return string_Match
