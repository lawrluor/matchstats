# Date converting/parsing utils

import re
import datetime
from datetime import date

# static dictionary to convert calendar date to datetime, used in convert_date
months = {'January' : 1,
          'February' : 2,
          'March' : 3,
          'April' : 4,
          'May' : 5,
          'June' : 6,
          'July' : 7, 
          'August' : 8, 
          'September' : 9,
          'October' : 10,
          'November' : 11,
          'December' : 12}

# Converts a date styled June 28, 2015 into datetime 2015-06-28
def convert_date(challonge_date):
  date_parser = re.compile('[/ ,-]+') 
  tokens = date_parser.split(challonge_date)
  # print tokens
  
  # integer representing month
  month = months[tokens[0]]
  day = int(tokens[1])
  year = int(tokens[2])
  # print month, day, year

  date = datetime.date(year=year, month=month, day=day)
  # print date
  return date

# Converts a date styled 06-28-2015 into datetime 2015-06-28
def convert_int_date(int_date):
  date_parser = re.compile('[/ ,-]+') 
  tokens = date_parser.split(int_date)
  # print tokens
  
  # integer representing month
  month = int(tokens[0])
  day = int(tokens[1])
  year = int(tokens[2])
  # print month, day, year

  date = datetime.date(year=year, month=month, day=day)
  # print date
  return date