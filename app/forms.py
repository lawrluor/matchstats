from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, SelectField, IntegerField, RadioField, SelectMultipleField, widgets # open fields to take input from person
from wtforms.validators import DataRequired, InputRequired, Required # checks to make sure field isn't empty

# main character choice list for SelectField; a constant list taken by SelectField containing all the characters and some special characters
main_char_choices = [('Fox', 'Fox'), ('Falco', 'Falco'), ('Sheik', 'Sheik'), ('Marth', 'Marth'), ('Jigglypuff', 'Jigglypuff'), ('Peach', 'Peach'), ('Captain Falcon', 'Captain Falcon'), ('Ice Climbers', 'Ice Climbers'), ('Dr. Mario', 'Dr. Mario'), ('Pikachu', 'Pikachu'), ('Samus', 'Samus'), ('Ganondorf', 'Ganondorf'), ('Luigi', 'Luigi'), ('Mario', 'Mario'), ('Young Link', 'Young Link'), ('Link', 'Link'), ('Donkey Kong', 'Donkey Kong'), ('Yoshi', 'Yoshi'), ('Zelda', 'Zelda'), ('Roy', 'Roy'), ('Mewtwo', 'Mewtwo'), ('Mr. Game and Watch', 'Mr. Game and Watch'), ('Ness', 'Ness'), ('Bowser', 'Bowser'), ('Pichu', 'Pichu'), ('Kirby', 'Kirby'), ('Random', 'Random'), ('Unchosen', 'Unchosen'), ('Multiple', 'Multiple')]

# secondaries character choice list for SelectField; a constant list taken by SelectField containing only the 26 SSBM Characters
secondaries_char_choices = [('Fox', 'Fox'), ('Falco', 'Falco'), ('Sheik', 'Sheik'), ('Marth', 'Marth'), ('Jigglypuff', 'Jigglypuff'), ('Peach', 'Peach'), ('Captain Falcon', 'Captain Falcon'), ('Ice Climbers', 'Ice Climbers'), ('Dr. Mario', 'Dr. Mario'), ('Pikachu', 'Pikachu'), ('Samus', 'Samus'), ('Ganondorf', 'Ganondorf'), ('Luigi', 'Luigi'), ('Mario', 'Mario'), ('Young Link', 'Young Link'), ('Link', 'Link'), ('Donkey Kong', 'Donkey Kong'), ('Yoshi', 'Yoshi'), ('Zelda', 'Zelda'), ('Roy', 'Roy'), ('Mewtwo', 'Mewtwo'), ('Mr. Game and Watch', 'Mr. Game and Watch'), ('Ness', 'Ness'), ('Bowser', 'Bowser'), ('Pichu', 'Pichu'), ('Kirby', 'Kirby')]


class UserCreate(Form):
  user_tag = StringField('tag', validators=[DataRequired()])
  user_region = StringField('region', validators=[DataRequired()])
  user_main = SelectField('main', choices=main_char_choices, coerce=str, validators=[DataRequired()])
  user_secondaries = SelectMultipleField('secondaries', choices=secondaries_char_choices, option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False), coerce=str)

class UserEdit(Form):
  edit_tag = StringField('tag', validators=[DataRequired()])
  edit_region = StringField('region', validators=[DataRequired()])
  edit_main= SelectField('main', choices=main_char_choices, validators=[DataRequired()])
  edit_secondaries = SelectMultipleField('secondaries', choices=secondaries_char_choices, option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))



class SetCreate(Form):
  set_tournament = StringField('tournament')
  set_winner_tag = StringField('winner_tag', validators=[DataRequired()])
  set_loser_tag = StringField('loser_tag', validators=[DataRequired()])
  set_winner_score = IntegerField('winner_score', validators=[InputRequired()])
  set_loser_score = IntegerField('loser_score', validators=[InputRequired()])
  set_max_match_count = SelectField('Best of:', choices = [('1','1'), ('3','3'), ('5','5'), ('7','7')], validators=[Required()]) # choices are strings, not integers, but are converted to integers in views.py - this is because it was buggy otherwise.

class MatchSubmit(Form):
  match_stage = SelectField('match_stage', choices = [('Battlefield', 'Battlefield'), ('Dream Land', 'Dream Land'), ('Final Destination', 'Final Destination'), ('Fountain of Dreams', 'Fountain of Dreams'), ('Pokemon Stadium', 'Pokemon Stadium'), ('Yoshi\'s Story', 'Yoshi\'s Story'), ('Other', 'Other')], coerce=str)

  # Data not required in case no match info is known (no validators for fields)
  match_winner = StringField('match_winner')
  match_loser = StringField('match_loser')
  winner_char = SelectField('winner_char', choices=main_char_choices)
  loser_char = SelectField('loser_char', choices=main_char_choices)

# SelectField format for choices: The first (value, label) is the actual value. The label is what appears in the dropdown menu. In this case, both should be the samei

#  Form generated when looking to search for head to head results between players
class HeadToHead(Form):
  user1 = StringField('user1', validators=[DataRequired()])
  user2 = StringField('user2', validators=[DataRequired()])

