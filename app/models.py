from app import db #imports database object from __init__.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  tag = db.Column(db.String(64), index=True, unique=True)
  main = db.Column(db.String(64), index=True)
  region = db.Column(db.String(128), index=True) #because db.String(128), need to cast this as a str when using it
  
  def __repr__(self):
    return '<User %s, Region %s, Main %s>' % (self.tag, self.region, self.main)
  
  def __str__(self):
    return self.tag + ' | Region: ' + str(self.region) + ' | Main: ' + self.main
  
  #getWonSets is a function that takes a user and returns the sets he has won.
  def getWonSets(self):
    sets_won = Set.query.filter(Set.winner_tag==self.tag).order_by(Set.id).all()
    return sets_won

  #getLostSets is a function that takes a user and returns the sets he has lost
  def getLostSets(self):
    sets_lost = Set.query.filter(Set.loser_tag==self.tag).order_by(Set.id).all()
    return sets_lost

  #getAllSets is a function that takes a user and returns all the sets he has played
  def getAllSets(self):
    all_sets = self.getWonSets() + self.getLostSets()
    return all_sets

#Set is the one in a one-to-many relationship with model Match
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
  
  def __str__(self): #String representation to be printed in html. Ex: Armada vs Mango: (3-2) Armada
    return self.winner_tag + '_' + str(self.winner_id) + ' vs ' + self.loser_tag + '_' + str(self.loser_id) + ': (' + str(self.winner_score) + '-' + str(self.loser_score) + ') ' + self.winner_tag
  
  #returns winner (user) of this set
  def getSetWinner(self):
    set_winner = User.query.filter(User.tag==self.winner_tag).first() 
    return set_winner #return winner_tag of the set, the User who won the set
  
  #returns winner ID (user.id) of a Set object
  def getSetWinnerID(self):
    set_winner = self.getSetWinner()
    return set_winner.id

  #returns loser ID (user.id) of a Set object
  def getSetLoserID(self):
    set_loser = self.getSetLoser()
    return set_loser.id

  #returns loser (user) of associated set
  def getSetLoser(self):
    set_loser = User.query.filter(User.tag==self.loser_tag).first()
    return set_loser

    
#Match is the many in a one-to-many relationship with model Set
class Match(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  set_id = db.Column(db.Integer, db.ForeignKey('set.id')) #relationship to Set
  stage = db.Column(db.String(128), index=True) #later map dictionary with stages?
  winner = db.Column(db.String(128), index=True)
  loser = db.Column(db.String(128), index=True)
  winner_char = db.Column(db.String(128), index=True)
  loser_char = db.Column(db.String(128), index=True)

  def __repr__(self):
    return '<Stage: %r, Winner: %r (%r), Loser: %r (%r)>' % (self.stage, self.winner, self.winner_char, self.loser, self.loser_char)

  def __str__(self): #String representation to be printed in html. Ex: Stage: Battlefield | Winner: Mango | Loser: Armada
    string_Match = 'Stage: ' + self.stage + ' | Winner: ' + self.winner + ' (' + str(self.winner_char) + ') | Loser: ' + self.loser + ' (' + str(self.loser_char) + ')'
    return string_Match
