import re

# Wrapper for regular expression compilation for mapping.
def compile_case_i_re(string):
  return re.compile(string, re.IGNORECASE)

# Make sure sanitized_list and regex_list are the same size or
# you might get an index out of bounds error.
# Params:
# tag - String containing tag to check.
# regex_list - Compiled regular expressions to check against the tag, a list of lists
# sanitized_list - Sanitized versions of the tag.
def sanitize_tag(tag, regex_list, sanitized_list):
  for i in range(len(regex_list)):
    if regex_list[i].match(tag):
      return sanitized_list[i]
  return tag

# Takes top_player_regex_raw_list as a parameter through map, meaning that each index is one list inside the list of regex expressions in top_player_regex_raw_list.
def add_prefixes(regex_list):
  wildcard = '.*'
  sep = '[\| \.`]'
  prefix = wildcard + sep
  prefix_list = []
   
  inner_list = []
  for i in range(len(regex_list)):
    inner_list.append(prefix + regex_list[i])

  joined_regex = '|'.join(inner_list)
  prefix_list.append(joined_regex)
  return joined_regex
    
"""
# Map function generating full regex list; appends special characters to top_player_regex_raw_list '[\| \.`].*' + 'mango'
def add_prefixes(regex_raw_list):
  wildcard = '.*'
  sep = '[\| \.`]'

  for i in range(len(regex_raw_list)):
    for j in range(len(regex_raw_list[i])):
      regex_raw_list[i][j] = wildcard.join(regex_raw_list[i][j])
      return regex_raw_list[i][j]
"""
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

wildcard = '.*'
sep = '[\| \.`]'
prefix = wildcard + sep

# Regular expressions representing top players.
top_player_regex_raw_list = map(add_prefixes, top_player_regex_raw_list)
"""
[
    [prefix + '(mang[o0])'],
    [prefix + '(armada)', prefix + '(\[a\]rmada)'],
    [prefix + '(ppmd)', prefix + '(dr\. pp)'],
    [prefix + '(mew2king)', prefix + '(m2k)'],
    [prefix + '(hungrybox)', prefix + '(hbox)'],
    [prefix + '(leffen)', prefix + '(l3ff3n)'],
    [prefix + '(axe)'],
    [prefix + '(hax)', prefix + '(hax\$)'],
    [prefix + '(westballz)'],
    [prefix + '(colbol)'],
    [prefix + '(fly amanita)'],
    [prefix + '(lucky)'],
    [prefix + '(pewpewu)', prefix + '(ppu)', prefix + '(pewpewyou)'],
    [prefix + '(shroomed)'],
    [prefix + '(silentwolf)'],
    [prefix + '(plup)'],
    [prefix + '(fiction)'],
    [prefix + '(s2j)'],
    [prefix + '(ice)'],
    [prefix + '(sfat)'],
    [prefix + '(zhu)'],
    [prefix + '(kirbykaze)', prefix + '(kk)'],
    [prefix + '(nintendude)'],
    [prefix + '(macd)'],
    [prefix + '(amsa)'],
    [prefix + '(chillindude)', prefix + '(chillindude829)'],
    [prefix + '(javi)'],
    [prefix + '(kels)'],
    [prefix + '(wizzrobe)', prefix + '(wizzy)'],
    [prefix + '(the moon)']
    ]
"""

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

top_player_regex_list = map(compile_case_i_re, top_player_regex_raw_list)

# Wrapper for sanitize_tag.
def check_and_sanitize_tag(tag):
  return sanitize_tag(tag, top_player_regex_list, sanitized_tags)
