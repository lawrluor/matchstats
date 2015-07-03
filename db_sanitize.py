#!flask/bin/python
import sys
from app import app, db, models
sys.path.append('./sanitize')
from sanitize_utils import check_and_sanitize_tag

def sanitize_users():
  users = models.User.query.all()
  for user in users:
    sanitized_tag = check_and_sanitize_tag(user.tag)
    if sanitized_tag and not sanitized_tag == user.tag:
      sanitized_user = models.User.query.filter(models.User.tag==sanitized_tag).first()
      if not sanitized_user:
        sanitized_user = models.User(tag=sanitized_tag)
        db.session.add(sanitized_user)
        db.session.commit()
      sanitize_sets(user, sanitized_user, sanitized_tag)
      db.session.delete(user)
      db.session.commit()

def sanitize_sets(user, sanitized_user, sanitized_tag):
  sets = user.getAllSets()
  for set_ in sets:
    if set_.winner_tag == user.tag:
      sanitize_matches(set_, sanitized_tag)
      set_.winner_tag = sanitized_tag
      set_.winner_id = sanitized_user.id
    elif set_.loser_tag == user.tag:
      sanitize_matches(set_, sanitized_tag)
      set_.loser_tag = sanitized_tag
      set_.loser_id = sanitized_user.id 

def sanitize_matches(set_, sanitized_tag):
  matches = set_.matches.all()
  for match in matches:
    if matches.winner == set_.winner_tag:
      matches.winner = sanitized_tag
    elif matches.loser == set_.loser_tag:
      matches.loser = sanitized_tag

def main():
  sanitize_users()

if __name__ == '__main__':
  main()
