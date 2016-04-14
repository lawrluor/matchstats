from parse_smashgg_info import *
from config import basedir
from app import app, db
from app.models import *

userlist = User.query.all()
print len(userlist)
emerald_city = parse_bracket_info("https://smash.gg/tournament/emerald-city-ii/brackets/11994/18349", "Emerald City Smash II", None, "April 9, 2016")

from parse_smashgg_info import *
ngp_49 = parse_bracket_info("https://smash.gg/tournament/new-game-plus-49/brackets/12509/26065/85665", "New Game Plus 49", "New England", "April 12, 2016")

def import_tournament_entrants(entrant_list, tournament_obj):
	for entrant in entrant_list:
		player_tag = entrant['player_tag']

		if tournament_obj.region:
			checked_player = check_set_user(player_tag, tournament_obj.region.region)
		else:
			checked_player = check_set_user(player_tag)
		print "CHECKED_PLAYER:", checked_player

		tournament_obj.placements.append(Placement(
										tournament_id=tournament_obj.id,
										tournament_name=tournament_obj.name,
										user_id=checked_player.id,
										placement=int(entrant['player_sub_placing'])
										))
		print "PLACEMENTS APPENDED"
	db.session.commit()
	return tournament_obj
	
def import_tournament_entrants(entrant_list, tournament_obj):
	print "TESTINGE IMPORT_TOURNAMENT_ENTRANTS"
	print tournament_obj, tournament_obj.region
	print len(entrant_list)
	for entrant in entrant_list:
		print "ENTRANT#", entrant, entrant['player_tag']
		player_tag = entrant['player_tag']
		
		# check or create new User object, tag=player_tag
      	if tournament_obj.region:
      		print "Region case"
        	checked_player = check_set_user(player_tag, tournament_obj.region.region)        	
      	else:
      		print "None case"
        	checked_player = check_set_user(player_tag)
      		
        print "CHECKED_PLAYER:", checked_player

      	# append relationship to Tournament as a Placement object; Placement objects are appended into a list in order of their User id, with no relation to their placing or tag.
      	tournament_obj.placements.append(Placement(tournament_id=tournament_obj.id,
                                    		tournament_name=tournament_obj.name,
                                        	user_id=checked_player.id,
                                        	placement=int(entrant['player_sub_placing'])
                                        	))
      	print "PLACEMENTS APPENDED"
  	db.session.commit()
  	return tournament_obj