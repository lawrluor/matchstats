from flask.ext.wtf import Form, validators
from wtforms import StringField, BooleanField, TextAreaField, SelectField, IntegerField, SelectMultipleField 
from wtforms.validators import DataRequired, InputRequired, Required, ValidationError, StopValidation

from app import app, db
from app.models import *
import re

# main character choice list for SelectField; a constant list taken by SelectField containing all the characters and some special characters
main_char_choices = [('Fox', 'Fox'),
                     ('Falco', 'Falco'), 
                     ('Sheik', 'Sheik'), 
                     ('Marth', 'Marth'), 
                     ('Jigglypuff', 'Jigglypuff'), 
                     ('Peach', 'Peach'), 
                     ('Captain Falcon', 'Captain Falcon'), 
                     ('Ice Climbers', 'Ice Climbers'), 
                     ('Dr. Mario', 'Dr. Mario'), 
                     ('Pikachu', 'Pikachu'), 
                     ('Samus', 'Samus'), 
                     ('Ganondorf', 'Ganondorf'), 
                     ('Luigi', 'Luigi'), 
                     ('Mario', 'Mario'), 
                     ('Young Link', 'Young Link'), 
                     ('Link', 'Link'), 
                     ('Donkey Kong', 'Donkey Kong'), 
                     ('Yoshi', 'Yoshi'), 
                     ('Zelda', 'Zelda'), 
                     ('Roy', 'Roy'), 
                     ('Mewtwo', 'Mewtwo'), 
                     ('Mr. Game and Watch', 'Mr. Game and Watch'), 
                     ('Ness', 'Ness'), 
                     ('Bowser', 'Bowser'), 
                     ('Pichu', 'Pichu'), 
                     ('Kirby', 'Kirby'), 
                     ('Random', 'Random'), 
                     ('Unknown', 'Unchosen'), 
                     ('Multiple', 'Multiple')]

# secondaries character choice list for SelectField; a constant list taken by SelectField containing only the 26 SSBM Characters
secondaries_char_choices = [('Fox', 'Fox'), 
                            ('Falco', 'Falco'), 
                            ('Sheik', 'Sheik'), 
                            ('Marth', 'Marth'), 
                            ('Jigglypuff', 'Jigglypuff'), 
                            ('Peach', 'Peach'), 
                            ('Captain Falcon', 'Captain Falcon'), 
                            ('Ice Climbers', 'Ice Climbers'), 
                            ('Dr. Mario', 'Dr. Mario'), 
                            ('Pikachu', 'Pikachu'), 
                            ('Samus', 'Samus'), 
                            ('Ganondorf', 'Ganondorf'), 
                            ('Luigi', 'Luigi'), 
                            ('Mario', 'Mario'), 
                            ('Young Link', 'Young Link'), 
                            ('Link', 'Link'), 
                            ('Donkey Kong', 'Donkey Kong'), 
                            ('Yoshi', 'Yoshi'), 
                            ('Zelda', 'Zelda'), 
                            ('Roy', 'Roy'), 
                            ('Mewtwo', 'Mewtwo'), 
                            ('Mr. Game and Watch', 'Mr. Game and Watch'), 
                            ('Ness', 'Ness'), 
                            ('Bowser', 'Bowser'), 
                            ('Pichu', 'Pichu'), 
                            ('Kirby', 'Kirby')]

# simple list of character strings for all possible main characters
main_char_list = ['Fox', 
                  'Falco', 
                  'Sheik', 
                  'Marth', 
                  'Jigglypuff', 
                  'Peach', 
                  'Captain Falcon', 
                  'Ice Climbers', 
                  'Dr. Mario', 
                  'Pikachu', 
                  'Samus', 
                  'Ganondorf', 
                  'Luigi', 
                  'Mario', 
                  'Young Link', 
                  'Link', 
                  'Donkey Kong', 
                  'Yoshi', 
                  'Zelda', 
                  'Roy', 
                  'Mewtwo', 
                  'Mr. Game and Watch', 
                  'Ness', 
                  'Bowser', 
                  'Pichu', 
                  'Kirby', 
                  'Random', 
                  'Unknown', 
                  'Multiple']

# simple list of character strings for all possible secondary characters
secondaries_char_list = ['Fox',
                         'Falco', 
                         'Sheik', 
                         'Marth', 
                         'Jigglypuff', 
                         'Peach', 
                         'Captain Falcon', 
                         'Ice Climbers', 
                         'Dr. Mario', 
                         'Pikachu', 
                         'Samus', 
                         'Ganondorf', 
                         'Luigi', 
                         'Mario', 
                         'Young Link', 
                         'Link', 
                         'Donkey Kong', 
                         'Yoshi', 
                         'Zelda', 
                         'Roy', 
                         'Mewtwo', 
                         'Mr. Game and Watch', 
                         'Ness', 
                         'Bowser', 
                         'Pichu', 
                         'Kirby'] 

# custom validator to check if two (User.tag) fields are not the same. This function format allows for other parameters besides (form, field)
def not_equal_to(fieldname):
  message = "Winner and Loser can't be the same!"

  def _not_equal_to(form, field, fieldname):
    if form.field == fieldname:
      raise ValidationError(message)

  return _not_equal_to

# custom validator to check that Set score can be converted to an integer, is a DQ value (-1), or is a 'W' or 'L' char
def set_score_check():
  message = "You must submit the Set score as an integer>=-1 and <10, or as a W/L character"

  def _set_score_check(form, field):
    score = field.data
    if score not in ['-1', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'W', 'L']:
      raise ValidationError(message)

  return _set_score_check

class UserCreate(Form):
  user_tag = StringField('tag', validators=[DataRequired()])
  user_region = StringField('region', validators=[DataRequired()])
  user_main = SelectField('main', choices=main_char_choices, coerce=str, validators=[DataRequired()])
  user_secondaries = SelectMultipleField('secondaries', choices=secondaries_char_choices, coerce=str)

class UserEdit(Form):
  edit_tag = StringField('tag', validators=[DataRequired()])
  edit_region = StringField('region', validators=[DataRequired()])
  edit_main= SelectField('main', choices=main_char_choices, validators=[DataRequired()])
  add_secondaries = SelectMultipleField('add_secondaries')
  remove_secondaries = SelectMultipleField('remove_secondaries') 

class SetCreate(Form):
  set_tournament = StringField('tournament')
  set_winner_tag = StringField('winner_tag', validators=[DataRequired()])
  set_loser_tag = StringField('loser_tag', validators=[DataRequired()])
  set_winner_score = StringField('winner_score', validators=[DataRequired(), set_score_check()]) 
  set_loser_score = StringField('loser_score', validators=[DataRequired(), set_score_check()])
  set_max_match_count = SelectField('Best of:', choices = [('1','1'), ('3','3'), ('5','5'), ('7','7')], validators=[Required()])
  no_match_info = BooleanField('no_match_info')

class SetEdit(Form):
  edit_tournament = StringField('tournament')
  edit_winner_tag = StringField('winner_tag', validators=[DataRequired()])
  edit_loser_tag = StringField('loser_tag', validators=[DataRequired()])
  edit_winner_score = IntegerField('winner_score', validators=[InputRequired()])
  edit_loser_score = IntegerField('loser_score', validators=[InputRequired()])
  edit_max_match_count = IntegerField('max_match_count', validators=[InputRequired()])
  edit_match_info = BooleanField('edit_match_info')

class MatchSubmit(Form):
  match_stage = SelectField('match_stage', choices = [('Battlefield', 'Battlefield'), ('Dream Land', 'Dream Land'), ('Final Destination', 'Final Destination'), ('Fountain of Dreams', 'Fountain of Dreams'), ('Pokemon Stadium', 'Pokemon Stadium'), ('Yoshi\'s Story', 'Yoshi\'s Story'), ('Other', 'Other')], coerce=str)

  # Data not required in case no match info is known (no validators for fields)
  match_winner = SelectField('match_winner', coerce=str)
  match_loser = SelectField('match_loser', coerce=str)
  winner_char = SelectField('winner_char', choices=main_char_choices, coerce=str)
  loser_char = SelectField('loser_char', choices=main_char_choices, coerce=str)

# SelectField format for choices: The first (value, label) is the actual value. The label is what appears in the dropdown menu. In this case, both should be the samei

#  Form generated when looking to search for head to head results between players
class HeadToHead(Form):
  user1 = StringField('user1', validators=[DataRequired()])
  user2 = StringField('user2', validators=[DataRequired()])

# search form in navigation bar
class SearchForm(Form):
  search = StringField('search', validators=[DataRequired()])

# select region form
class RegionSelect(Form):
  region_name = SelectField('region_name', coerce=str)
