#!flask/bin/python

import re
from app import app, db
from app.models import *

def compile_case_i_re(string):
  return re.compile(string, re.IGNORECASE)

top_player_regex_raw_list = [
    '.*(mang[o0])',
    '.*(armada)',
    '.*(ppmd)|.*(dr\. pp)',
    '.*(mew2king)|.*(m2k)',
    '.*(hungrybox)|.*(hbox)',
    '.*(leffen)|.*(l3ff3n)',
    '.*(axe)',
    '.*(hax)|.*(hax\$)',
    '.*(westballz)',
    '.*(colbol)',
    '.*(fly amanita)',
    '.*(lucky)',
    '.*(pewpewu)|.*(ppu)',
    '.*(shroomed)',
    '.*(silentwolf)',
    '.*(plup)',
    '.*(fiction)',
    '.*(s2j)',
    '.*(amsa)'
    ]

sanitized_tags = [
    'mango',
    'armada',
    'ppmd',
    'mew2king',
    'hungrybox',
    'leffen',
    'axe',
    'hax',
    'westballz',
    'colbol',
    'fly amanita',
    'lucky',
    'pewpewu',
    'shroomed',
    'silentwolf',
    'plup',
    'fiction',
    's2j',
    'amsa'
    ]

top_player_regex_list = map(compile_case_i_re, top_player_regex_raw_list)


# Make sure sanitized_list and regex_list are the same size.
def sanitize_tag(tag, regex_list, sanitized_list):
  for i in range(len(regex_list)):
    if regex_list[i].match(tag):
      return sanitized_list[i]


fake_userlist = ['Cloud 9 | Mango', 'C9 Mang0', 'Mango',
								'Alliance | Armada', 'P4K EMP Armada', 
								'Evil Geniuses | PPMD', 'EG | PPMD', 'Dr. PP',
								'MVG | Mew2King', 'P4K EMP Mew2King', 'M2K',
								'Curse | Hungrybox', 'Crs.Hungrybox', 'Liquid` Hungrybox', 'Liquid Hungrybox',
								'TSM | Leffen', 'Leffen',
								'MVG | Axe', 'MOR Axe', 'MOR | Axe',
								'VGBC | Hax',
								'Westballz',
								'SS | Colbol',
								'CLG | PewPewU', 'MIOM : PewPewU', 'PPU',
								'MMG Shroomed',
								'lucky',
								'VGBC | aMSa']

top_player_list = ['mango', 'armada', 'ppmd', 'mew2king', 'hungrybox', 
									'leffen', 'axe', 'hax', 'westballz', 'colbol',
									'fly amanita', 'lucky', 'pewpewu', 'shroomed', 'silentwolf',
									'plup', 'fiction', 's2j', 'ice', 'sfat', 
									'zhu', 'amsa', 'kirbykaze', 'nintendude', 'macd']


for tag in fake_userlist:
  print tag 
  print sanitize_tag(tag, top_player_regex_list, sanitized_tags) + '\n'

print sanitize_tag("amsa", top_player_regex_list, sanitized_tags)

#for user_tag in fake_userlist:
#	# remove sponsorship dividers or other unwanted characters, and make lowercase
#	normalized_tag = user_tag.lower()
#	for player in top_player_list:
#		tag_start = normalized_tag.find(player)
#		if tag_start != -1:
#			# if found a substring, this should be the user's true tag.
#			print normalized_tag
#			tag = normalized_tag[tag_start:]
#			print tag
#
#			# check for chars before the tag substring; these should be teams or sponsors preceding the true tag.
#			# take out whitespace and extraneous characters that divide the tag
#			team = normalized_tag[:tag_start]
#			team = team.strip('|`.: ')
#			print team
#			print len(team)
#
#	print '\n'

"""
# query database
userlist = User.query.all()
for user in userlist:
	do stuff
"""
