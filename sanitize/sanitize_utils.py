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
  sep = '[|.`\' ]'
  prefix = wildcard + sep
  prefix_list = []
   
  inner_list = []
  for regex in regex_list:
    inner_list.append(prefix + regex)
    inner_list.append(regex)

  joined_regex = '|'.join(inner_list)
  prefix_list.append(joined_regex)
  return joined_regex
    
# Raw Regular expression list representing top players, to be processed by add_prefixes
top_player_regex_raw_list = [
    ['(mang[o0])', '(c9mang[o0])'],
    ['(armada)', '(\[a\]rmada)'],
    ['(ppmd)', '(dr\. pp)', '(dr\. peepee)', '(dr pp)', '(dr peepee)', '(doctor pp)', '(doctor peepee)'],
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
    ['(silentwolf)', '(silent wolf)'],
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
    ['(chillindude)', '(chillindude829)', '(chillin)'],
    ['(javi)'],
    ['(kels)'],
    ['(wizzrobe)', '(wizzy)'],
    ['(the moon)', '(la luna)'],
    ['(eddy mexico)'],
    ['(chu dat)', '(chudat)'],
    ['(bladewise)'],
    ['(abate)'],
    ['(zer[o0])'],
    ['(larry lurr)', '(larrylurr)', '(DEHF)'],
    ['(hugs)', '(hugs86)'],
    ['(duck)'],
    ['(dj nintendo)', '(djn)'],
    ['(kalamazhu)', '(kalamazhoo)', '(kzhu)'],
    ['(lord)'],
    ['(cactuar)', '(cactus)'],
    ['(weon-x)', '(weon x)', '(weonx)'],
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
    ['(darrell)', '(darell)', '(darrel)'],
    ['(sl[o0]x)'],
    ['(beer man)', '(beer master)', '(lambchops)'],
    ['(s[o0]ft)'],
    ['(fuzzyness)'],
    ['(taf[o0]kints)', '(taf[o0])'],
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
    ['([bj]izzarro flame)', '([bj]izzarroflame)', '([bj]izaro flame)', '([bj]izzaro flame)', '([bj]izarro flame)'],
    ['(hyprid)'],
    ['(a[zs]u[sz]a)'],
    ['(m[o0]j[o0])'],
    ['(milkman)', '(milk man)'],
    ['(frootloop)'],
    ['(esam)'],
    # MIOM 2013 Rank Begins
    ['(wobbles)', '(wobbles the phoenix)'],
    ['(unknown522)', '(unknown 522)', '(ryan ford)'],
    ['(taj)'],
    ['(overtriforce)', '(over)', '(over triforce)'],
    ['(dashizwiz)', '(shiz)', '(da shiz wiz)'],
    ['(vwins)'],
    ['(th[o0]rn)'],
    ['(lovage)'],
    ['(jman)'],
    ['(gucci)'],
    ['(blunted_object10)', '(blunted_object)', '(blunted object)'],
    ['(bam)'],
    ['(sung666)', '(sung 666)', '(sung)'],
    ['(eggz)'],
    ['(strawhat dahean)', '(strawhat)'],
    ['(vish)'],
    ['(sion)'],
    ['(phil)'],
    ['(bob\$)'],
    ['(kounotori)'],
    ['(stab)', '(victor abdul latif)', '(stabbedbyahippie)', '(stabbedbyanipple)'],
    ['(g\$)'],
    ['(vist)'],
    ['(pkmvodka)', '(pkm vodka)']
    ]

# NE Top Players start here
NE_player_regex_list = [
    ['(koreandj)', '(korean dj)', '(kdj)'],
    ['(swiftbass)', '(swift)', '(gibson zero)', '(gibsonzero)'],
    ['(z[o0]s[o0])'],
    ['(th[o0]rn)'],
    ['(crush)'],
    ['(mafia)', '(irish mafia)', '(slimjim)', '(slim jim)'], 
    ['(mdz)', '(mattdotzeb)', '(matt dot zeb)'],
    ['(klap[s$])'],
    ['(tian)'],
    ['(squible)'],
    ['(kyupuff)', '(kyu puff)'],
    ['(rime)'],
    ['(mr lemon)', '(mr. lemon)']
    ]

# Sanitized tags representing global top players.
sanitized_tags = [
    'Mango',
    'Armada',
    'PPMD',
    'Mew2King',
    'Hungrybox',
    'Leffen',
    'Axe',
    'Hax',
    'Westballz',
    'Colbol',
    'Fly Amanita',
    'Lucky',
    'PewPewU',
    'Shroomed',
    'Silentwolf',
    'Plup',
    'Fiction',
    'S2J',
    'Ice',
    'SFAT',
    'Zhu',
    'Kirbykaze',
    'Nintendude',
    'MacD',
    'aMSa',
    'Chillindude',
    'Javi',
    'Kels',
    'Wizzrobe',
    'The Moon',
    'Eddy Mexico',
    'ChuDat',
    'Bladewise',
    'Abate',
    'Zero',
    'Larry Lurr',
    'HugS',
    'Duck',
    'DJ Nintendo',
    'Kalamazhu',
    'Lord',
    'Cactuar',
    'Weon-X',
    'Darkrain',
    'Kage',
    'Zanguzen',
    'SilentSpectre',
    'KoreanDJ',
    'Swift',
    'Zoso',
    'Raynex',
    'Darkatma',
    'Porkchops',
    'I.B.',
    'Darc',
    'Swedish Delight',
    'OkamiBW',
    'Ken',
    'Vanz',
    'Excel Zero',
    'Darrell',
    'Slox',
    'Lambchops',
    'S0ft',
    'Fuzzyness',
    'Tafokints',
    'Santi',
    'Dart',
    'Blea Gelo',
    'Redd',
    'Hanky Panky',
    'Remen',
    'Stricnyn3',
    'Cyrain',
    'HomeMadeWaffles',
    'Pikachad',
    'Reno',
    'Gahtzu',
    'DOH',
    'Eggm',
    'Arc',
    'Tope',
    'Druggedfox',
    'Gravy',
    'Tai',
    'Lucien',
    'Lord HDL',
    'Trail',
    'Scar',
    'Laudandus',
    'Toph',
    'Alex19',
    'Connorthekid',
    'Bizzarro Flame',
    'Hyprid',
    'Azusa',
    'Mojo',
    'Milkman',
    'Frootloop',
    'ESAM',
    # 2013 MIOM Rank List Begins
    'Wobbles',
    'Unknown522',
    'Taj',
    'Overtriforce',
    'DaShizWiz',
    'Vwins',
    'Th0rn',
    'Lovage',
    'Jman',
    'Gucci',
    'Blunted_object10',
    'Bam',
    'Sung666',
    'Eggz',
    'Strawhat Dahean',
    'Vish',
    'Sion',
    'Phil',
    'Bob\$',
    'Kounotori',
    'Stab',
    'G\$',
    'Vist',
    'Pkmvodka'
    ]

    # NE Top Players begin here
NE_sanitized_tags = [
    'KoreanDJ',
    'Swift',
    'Zoso',
    'Thorn',
    'Crush',
    'Mafia',
    'Mattdotzeb',
    'Klap$',
    'Tian',
    'Squible',
    'Kyu Puff',
    'Rime',
    'Mr. Lemon'
    ]

# if region==None or region==Global:
  # prefixed_player_regex_list = map(add_prefixes, top_player_regex_raw_list)
  # player_regex_list = 
# else:
  # if region in Regex_list_dict:
    # prefixed_player_regex_list = map(add_prefixes, top_player_regex_raw_list)
    # player_regex_list = map(compile_case_i_re, top_player_regex_raw_list)

# Convert top_player_regex_raw_list to a version with regular expression prefixes wildcard and sep added
prefixed_player_regex_list = map(add_prefixes, top_player_regex_raw_list)

# Convert the list with prefixes added to all lowercase tags
player_regex_list = map(compile_case_i_re, prefixed_player_regex_list)

# Wrapper for sanitize_tag.
def check_and_sanitize_tag(tag): #region is other parameter
  return sanitize_tag(tag, player_regex_list, sanitized_tags)
  #return sanitize_tag(tag, NE_player_regex_list, NE_sanitized_tags)
