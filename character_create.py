#!flask/bin/python

from config import basedir
from app import app, db
from app.models import *

print "Print current Character database"
characterlist = Character.query.all()
print characterlist
print '\n'

# Create all Character objects
Fox = Character(id=1, name='Fox')
Falco = Character(id=2, name='Falco')
Sheik = Character(id=3, name='Sheik')
Marth = Character(id=4, name='Marth')
Jigglypuff = Character(id=5, name='Jigglypuff')
Peach = Character(id=6, name='Peach')
Captain_Falcon = Character(id=7, name='Captain Falcon')
Ice_Climbers = Character(id=8, name='Ice Climbers')
Dr_Mario = Character(id=9, name='Dr. Mario')
Pikachu = Character(id=10, name='Pikachu')
Samus = Character(id=11, name='Samus')
Ganondorf = Character(id=12, name='Ganondorf')
Luigi = Character(id=13, name='Luigi')
Mario = Character(id=14, name='Mario')
Young_Link = Character(id=15, name='Young Link')
Link = Character(id=16, name='Link')
Donkey_Kong = Character(id=17, name='Donkey Kong')
Yoshi = Character(id=18, name='Yoshi')
Zelda = Character(id=19, name='Zelda')
Roy = Character(id=20, name='Roy')
Mewtwo = Character(id=21, name='Mewtwo')
Mr_Game_and_Watch = Character(id=22, name='Mr. Game and Watch')
Ness = Character(id=23, name='Ness')
Bowser = Character(id=24, name='Bowser')
Pichu = Character(id=25, name='Pichu')
Kirby = Character(id=26, name='Kirby')
Random = Character(id=27, name='Random')
Unchosen = Character(id=28, name='Unchosen')
Multiple = Character(id=29, name='Multiple')

db.session.add(Fox)
db.session.add(Falco)
db.session.add(Sheik)
db.session.add(Marth)
db.session.add(Jigglypuff)
db.session.add(Peach)
db.session.add(Captain_Falcon)
db.session.add(Ice_Climbers)
db.session.add(Dr_Mario)
db.session.add(Pikachu)
db.session.add(Samus)
db.session.add(Ganondorf)
db.session.add(Luigi)
db.session.add(Mario)
db.session.add(Young_Link)
db.session.add(Link)
db.session.add(Donkey_Kong)
db.session.add(Yoshi)
db.session.add(Zelda)
db.session.add(Roy)
db.session.add(Mewtwo)
db.session.add(Mr_Game_and_Watch)
db.session.add(Ness)
db.session.add(Bowser)
db.session.add(Pichu)
db.session.add(Kirby)
db.session.add(Random)
db.session.add(Unchosen)
db.session.add(Multiple)

db.session.commit()

print "Print new Character database"
characterlist = Character.query.all()
print characterlist