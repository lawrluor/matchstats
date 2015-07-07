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
      print regex_list[i]
      return sanitized_list[i]
  return tag

# Takes top_player_regex_raw_list as a parameter through map, meaning that each index is one list inside the list of regex expressions in top_player_regex_raw_list.
def add_prefixes(regex_list):
  wildcard = '.*'
  sep = '[|.` ]'
  prefix = wildcard + sep
  prefix_list = []
   
  inner_list = []
  for regex in regex_list:
    inner_list.append(prefix + regex)
    inner_list.append(regex)

  joined_regex = '|'.join(inner_list)
  prefix_list.append(joined_regex)
  return joined_regex
    
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
    ['(s2j)', '(smoke2jointz)'],
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
    ['(the moon)'],
    ['(eddy mexico)'],
    ['(chu dat)', '(chudat)'],
    ['(bladewise)'],
    ['(abate)'],
    ['(zer[o0])'],
    ['(larry lurr)', '(larrylurr)', '(DEHF)'],
    ['(hugs)', '(hugs86)'],
    ['(duck)'],
    ['(dj nintentdo)', '(djn)'],
    ['(kalamazhu)', '(kalamazhoo)', '(kzhu)'],
    ['(lord)'],
    ['(cactuar)', '(cactus)'],
    ['(weon[- ]x)', '(weonx)'],
    ['(darkrain)'],
    ['(kage)', '(kage the warrior)'],
    ['(zanguzen)'],
    ['(silentspect[er][re])', '(silent spect[er][re])'],
    ['(koreandj)', '(korean dj)', '(kdj)'],
    ['(swiftbass)', '(swift)', '(gibson zero)', '(gibsonzero)'],
    ['(z[o0]s[o0])'],
    ['(raynex)'],
    ['(darkatma)', '(atma)'],
    ['(porkchops)'],
    ['(ib)', '(i\.b\.)'],
    ['(darc)'],
    ['(swedish delight)', '(swedish)'],
    ['(okamibw)', '(okami bw)', '(okami)'],
    ['(ken)', '(sephiroth ken)', '(sephirothken)'],
    ['(vanz)'],
    ['(excel zer[o0])', '(excelzero)'],
    ['(darrell)'],
    ['(sl[o0]x)'],
    ['(beer man)', '(lambchops)'],
    ['(s[o0]ft)'],
    ['(fuzzyness)'],
    ['(taf[o0]kints)'],
    ['(lil fumi)', '(santi)', '(santiago)'],
    ['(dart)', '(dart!)'],
    ['(blea gelo)', '(bleagelo)'],
    ['(redd)'],
    ['(hanky panky)', '(hankypanky)'],
    ['(remen)'],
    ['(str[1i]cn[1iy]n[e3])', '(str[1i]c9)', '(str[1i]c n[1iy]n[e3])', '(str[1i]c 9)'],
    ['(cyrain)'],
    ['(homemadewaffles)', '(hmw)', '(yung waff)'],
    ['(pikachad)', '(pika chad)'],
    ['(ren[o0])'],
    ['(gahtzu)', '(ghatzu)'],
    ['(doh)', '(darkness of heart)'],
    ['(eggm)'],
    ['(arc)'],
    ['(t[o0]pe)'],
    ['(drugged fox)', '(druggedfox)'],
    ['(gravy)'],
    ['(tai)'],
    ['(lucien)'],
    ['(lord hdl)', '(lordhdl)'],
    ['(trail)'],
    ['(scar)'],
    ['(laudandus)'],
    ['(t[o0]ph)'],
    ['(alex19)'],
    ['(c[o0]nn[o0]rthekid)', '(c[o0]nn[o0]r)', '(c[o0]nn[o0]r the kid)'],
    ['([bj]izzarro flame)', '([bj]izzarroflame)'],
    ['(hyprid)'],
    ['(a[zs]u[sz]a)'],
    ['(m[o0]j[o0])'],
    ['(milkman)', '(milk man)'],
    ['(frootloop)'],
    ['(esam)']
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
    'the moon',
    'eddy mexico',
    'chu dat',
    'bladewise',
    'abate',
    'zero',
    'larry lurr',
    'hugs',
    'duck',
    'dj nintendo',
    'kalamazhu',
    'lord',
    'cactuar',
    'weon-x',
    'darkrain',
    'kage',
    'zanguzen',
    'silentspectre',
    'koreandj',
    'swift',
    'zoso',
    'raynex',
    'darkatma',
    'porkchops',
    'ib',
    'darc',
    'swedish delight',
    'okamibw',
    'ken',
    'vanz',
    'excel zero',
    'darrell',
    'slox',
    'lambchops',
    's0ft',
    'fuzzyness',
    'tafokints',
    'santi',
    'dart',
    'blea gelo',
    'redd',
    'hanky panky',
    'remen',
    'stricnyn3',
    'cyrain',
    'homemadewaffles',
    'pikachad',
    'reno',
    'gahtzu',
    'doh',
    'eggm',
    'arc',
    'tope',
    'druggedfox',
    'gravy',
    'tai',
    'lucien',
    'lord hdl',
    'trail',
    'scar',
    'laudandus',
    'toph',
    'alex19',
    'connorthekid',
    'bizzarro flame',
    'hyprid',
    'azusa',
    'mojo',
    'milkman',
    'frootloop',
    'esam'
    ]
   
# Convert top_player_regex_raw_list to a version with regular expression prefixes wildcard and sep added
top_player_regex_raw_list = map(add_prefixes, top_player_regex_raw_list)

# Convert the list with prefixes added to all lowercase tags
top_player_regex_list = map(compile_case_i_re, top_player_regex_raw_list)

# Wrapper for sanitize_tag.
def check_and_sanitize_tag(tag):
  return sanitize_tag(tag, top_player_regex_list, sanitized_tags)
