import re

# Wrapper for regular expression compilation for mapping.
def compile_case_i_re(string):
  return re.compile(string, re.IGNORECASE)

# Make sure sanitized_list and regex_list are the same size or
# you might get an index out of bounds error.
# Params:
# tag - String containing tag to check.
# regex_list - Compiled regular expressions to check against the tag.
# sanitized_list - Sanitized versions of the tag.
def sanitize_tag(tag, regex_list, sanitized_list):
  for i in range(len(regex_list)):
    if regex_list[i].match(tag):
      return sanitized_list[i]
  return tag


# Regular expressions representing top players.
top_player_regex_raw_list = [
    '.*(mang[o0])',
    '.*(armada)|.*(\[a\]rmada).*',
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
    'amsa'
    ]

top_player_regex_list = map(compile_case_i_re, top_player_regex_raw_list)

# Wrapper for sanitize_tag.
def check_and_sanitize_tag(tag):
  return sanitize_tag(tag, top_player_regex_list, sanitized_tags)
