from parse_smashgg_info import *
from config import basedir
from app import app, db
from app.models import *

emerald_city = parse_bracket_info("https://smash.gg/tournament/emerald-city-ii/brackets/11994/18349", "Emerald City Smash II", None, "April 9, 2016")
iny = parse_bracket_info("https://smash.gg/tournament/i-m-not-yelling-feat-armada/brackets/10003/1137/1690", "I'm Not Yelling", None, "April 11, 2015")

from parse_smashgg_info import *
ngp_49 = parse_bracket_info("https://smash.gg/tournament/new-game-plus-49/brackets/12509/26065/85665", "New Game Plus 49", "New England", "April 12, 2016")


# order by trueskills: session.query(Base).join(Base.owner).order_by(Player.name)
users = User.query.join(User.trueskills).order_by(TrueSkill.cons_mu.desc()).all()
for user in users:
	print user