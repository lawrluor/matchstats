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
    for j in range(len(regex_list[i])):
      if regex_list[i][j].match(tag):
        return sanitized_list[i]
  return tag

# Map function generating full regex list; appends special characters to top_player_regex_raw_list '[\| \.`].*' + 'mango'
def add_prefixes(regex_raw_list):
  wildcard = '.*'
  sep = '[\| \.`]'

  for i in range(len(regex_raw_list)):
    for j in range(len(regex_raw_list[i])):
      regex_raw_list[i][j] = wildcard  + regex_raw_list[i][j]
      return regex_raw_list[i][j]

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

top_player_regex_raw_list = map(add_prefixes, top_player_regex_raw_list)


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
