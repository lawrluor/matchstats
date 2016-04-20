from challonge_parse import *
from config import basedir
from app import app, db
from app.models import *
import challonge

# Test Authorization
challonge.set_credentials("ssbtonic", "55TSSgywjR2bPpvIXDMrm5pZ6edm6Iq0rmcCXK5c")
challonge.get_credentials()
# parse_url("http://bigbluees.challonge.com/NGP46")
# parse_url("http://challonge.com/fi2f9gcu")
# 2372209


process_tournament("http://bigbluees.challonge.com/NGP47", "NGP 47", "New England", "March 29, 2016")
process_tournament("http://bigbluees.challonge.com/NGP45", "NGP 45", "New England", "March 15, 2016")
process_tournament("http://bigbluees.challonge.com/NGP46", "NGP 46", "New England", "March 22, 2016")