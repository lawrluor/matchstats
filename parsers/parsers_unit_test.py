from parse_smashgg_info import *
from challonge_parse import *
from config import basedir
from app import app, db
from app.models import *

import challonge

print "---TESTING SMASHGG FUNCTIONS---"
# Multi-level tournament, with many sub_brackets
emerald_city = parse_bracket_info("https://smash.gg/tournament/emerald-city-ii/brackets/11994/18349", "Emerald City Smash II", None, "April 9, 2016")

# Single-level tournament, where main tournament is the final bracket. NOTE THE DIFFERENT URLS
ngp_49 = parse_bracket_info("https://smash.gg/tournament/new-game-plus-49/brackets/12509/26065/85665", "New Game Plus 49", "New England", "April 12, 2016")
iny = parse_bracket_info("https://smash.gg/tournament/i-m-not-yelling-feat-armada/brackets/10003/1137/1690", "I'm Not Yelling", None, "April 11, 2015")


print "---TESTING CHALLONGE FUNCTIONS---"
# Test Authorization
challonge.set_credentials("ssbtonic", "55TSSgywjR2bPpvIXDMrm5pZ6edm6Iq0rmcCXK5c")
challonge.get_credentials()

process_tournament("http://bigbluees.challonge.com/NGP47", "NGP 47", "New England", "March 29, 2016")
process_tournament("http://bigbluees.challonge.com/NGP45", "NGP 45", "New England", "March 15, 2016")
process_tournament("http://bigbluees.challonge.com/NGP46", "NGP 46", "New England", "March 22, 2016")

# order by trueskills: session.query(Base).join(Base.owner).order_by(Player.name)
users = User.query.join(User.trueskills).order_by(TrueSkill.cons_mu.desc()).all()
for user in users:
	print user