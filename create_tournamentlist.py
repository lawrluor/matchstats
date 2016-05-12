import re
import sys

import challonge

def main():
  user_list  = sys.argv[1]
  tournamentlist_filename = sys.argv[2]
  find_tournaments(user_list, tournamentlist_filename)
    
challonge.set_credentials("ssbtonic", "55TSSgywjR2bPpvIXDMrm5pZ6edm6Iq0rmcCXK5c")

def find_tournaments(user_list, tournamentlist_filename):
  tournaments = []
  names = []
  urls = []
  dates = []
  with open(user_list, 'r') as f:
    for user in f:
      tournaments = challonge.tournaments.index("all", "double_elimination", "2000-01-01", "2020-01-01", user)
      for tournament in tournaments:
        names.append(tournament["name"])
        urls.append(tournament["full_challonge_url"])
        date = tournament["updated_at"][:10].replace("-","/")
        formatted_date = date[6:] + date[:7]
        dates.append(formatted_date)
  f.close()
  
  with open(tournamentlist_filename, 'w') as f:
    for name, url, date in zip(names, urls, dates):
      f.write(name+"|"+url+"|"+date)
  f.close()
      
if __name__== "__main__":
  main()
