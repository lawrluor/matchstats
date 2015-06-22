from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField, IntegerField # open fields to take input from person
from wtforms.validators import DataRequired, InputRequired, Required # checks to make sure field isn't empty

class UserCreate(Form):
  user_tag = StringField('tag', validators=[DataRequired()])
  user_region = StringField('region', validators=[DataRequired()])
  user_main = StringField('main', validators=[DataRequired()])

class SetCreate(Form):
  set_winner_tag = StringField('winner_tag', validators=[DataRequired()])
  set_loser_tag = StringField('loser_tag', validators=[DataRequired()])
  set_winner_score = IntegerField('winner_score', validators=[InputRequired()])
  set_loser_score = IntegerField('loser_score', validators=[InputRequired()])
  set_max_match_count = SelectField('Best of:', choices = [('1','1'), ('3','3'), ('5','5'), ('7','7')], validators=[Required()]) # choices are strings, not integers, but are converted to integers in views.py - this is because it was buggy otherwise.

class MatchSubmit(Form):
  char_list = [('Fox', 'Fox'), ('Falco', 'Falco'), ('Sheik', 'Sheik'), ('Marth', 'Marth'), ('Jigglypuff', 'Jigglypuff'), ('Peach', 'Peach'), ('Captain Falcon', 'Captain Falcon'), ('Ice Climbers', 'Ice Climbers')] # Choices list for winner_char and loser_char SelectField; a constant value containing all the characters and not an input
  
  match_stage = SelectField('match_stage', choices = [('Battlefield', 'Battlefield'), ('Dream Land', 'Dream Land'), ('Final Destination', 'Final Destination'), ('Fountain of Dreams', 'Fountain of Dreams'), ('Pokemon Stadium', 'Pokemon Stadium'), ('Yoshi\'s Story', 'Yoshi\'s Story'), ('Other', 'Other')], coerce=str, validators=[Required()]) # optional input, so doesn't check if left blank
  
  match_winner = StringField('match_winner')
  match_loser = StringField('match_loser')
  winner_char = SelectField('winner_char', choices=char_list) # Data no required in case no match info is known
  loser_char = SelectField('loser_char', choices=char_list)

# SelectField format for choices: The first (value, label) is the actual value. The label is what appears in the dropdown menu. In this case, both should be the samei

#  Form generated when looking to search for head to head results between players
class HeadToHead(Form):
  user1 = StringField('user1', validators=[DataRequired()])
  user2 = StringField('user2', validators=[DataRequired()])

