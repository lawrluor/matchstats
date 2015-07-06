#!flask/bin/python

import re
from sanitize_utils import add_prefixes

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

# Regular expressions representing top players.
top_player_regex_raw_list = [
    ['(mang[o0])'],
    ['(armada)', '(\[a\]rmada)'],
    ['(ppmd)', '(dr\. pp)'],
    ['(mew2king)', '(m2k)'],
    ['(hungrybox)', '(hbox)'],
    ['(leffen)', '(l3ff3n)'],
    ['(axe)'],
    ['(hax)', '(hax\$)'],
    ['(westballz)'],
    ['(colbol)'],
    ['(fly amanita)'],
    ['(lucky)'],
    ['(pewpewu)', '(ppu)', '(pewpewyou)'],
    ['(shroomed)'],
    ['(silentwolf)'],
    ['(plup)'],
    ['(fiction)'],
    ['(s2j)'],
    ['(ice)'],
    ['(sfat)'],
    ['(zhu)'],
    ['(kirbykaze)', '(kk)'],
    ['(nintendude)'],
    ['(macd)'],
    ['(amsa)'],
    ['(chillindude)', '(chillindude829)'],
    ['(javi)'],
    ['(kels)'],
    ['(wizzrobe)', '(wizzy)'],
    ['(the moon)']
    ]

# Sanitized tags representing top players.
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
    'ice',
    'sfat',
    'zhu',
    'kirbykaze',
    'nintendude',
    'macd',
    'amsa',
    'chillindude',
    'javi',
    'kels',
    'wizzrobe',
    'the moon'
    ]

print top_player_regex_raw_list
top_player_regex_raw_list = map(add_prefixes, top_player_regex_raw_list)
print top_player_regex_raw_list

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
