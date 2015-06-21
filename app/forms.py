from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField, IntegerField #open fields to take input from person
from wtforms.validators import DataRequired, InputRequired, Required #checks to make sure field isn't empty

class UserCreate(Form):
  user_tag = StringField('tag', validators=[DataRequired()])
  user_region = StringField('region', validators=[DataRequired()])
  user_main = StringField('main', validators=[DataRequired()])

class SetCreate(Form):
  set_winner_tag = StringField('winner_tag', validators=[DataRequired()])
  set_loser_tag = StringField('loser_tag', validators=[DataRequired()])
  set_winner_score = IntegerField('winner_score', validators=[InputRequired()])
  set_loser_score = IntegerField('loser_score', validators=[InputRequired()])
  set_max_match_count = SelectField('Best of:', choices = [('1','1'), ('3','3'), ('5','5'), ('7','7')], validators=[Required()]) #choices are strings, not integers, but are converted to integers in views.py - this is because it was buggy otherwise.

class MatchSubmit(Form):
  match_stage = SelectField('match_stage', choices = [('Battlefield', 'Battlefield'), ('Dream Land', 'Dream Land'), ('Final Destination', 'Final Destination'), ('Fountain of Dreams', 'Fountain of Dreams'), ('Pokemon Stadium', 'Pokemon Stadium'), ('Yoshi\'s Story', 'Yoshi\'s Story'), ('Other', 'Other')], coerce=str, validators=[Required()]) #optional input, so doesn't check if left blank
  match_winner = StringField('match_winner')
  match_loser = StringField('match_loser')
  winner_char = StringField('winner_char')
  loser_char = StringField('loser_char')

#SelectField format for choices: The first (value, label) is the actual value. The label is what appears in the dropdown menu. In this case, both should be the same
