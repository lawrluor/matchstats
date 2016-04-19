from challonge_parse import *
from config import basedir
from app import app, db
from app.models import *
import challonge

# Test Authorization
challonge.set_credentials("ssbtonic", "55TSSgywjR2bPpvIXDMrm5pZ6edm6Iq0rmcCXK5c")
challonge.get_credentials()

process_tournament(2372209, "NGP 49", "New England", "March 29, 2016")
