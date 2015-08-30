import re
from collections import defaultdict
    
# Raw Regular expression list representing top players, to be processed by add_prefixes
player_raw_regex_dict = {
    'Global' : [
    ['(mang[o0]$)', '(c9mang[o0]$)'],
    ['(armada$)', '(\[a\]rmada$)'],
    ['(ppmd$)', '(dr\. pp$)', '(dr\. peepee$)', '(dr pp$)', '(dr peepee$)', '(doctor pp$)', '(doctor peepee$)'],
    ['(mew2king$)', '(m2k$)'],
    ['(hungrybox$)', '(hbox$)'],
    ['(leffen$)', '(l3ff3n$)'],
    ['(axe$)'],
    ['(hax$)', '(hax\$$)'],
    ['(westballz$)'],
    ['(colbol$)'],
    ['(fly amanita$)'],
    ['(lucky$)'],
    ['(pewpewu$)', '(ppu$)', '(pewpewyou$)'],
    ['(shroomed$)'],
    ['(silentwolf$)', '(silent wolf$)'],
    ['(plup$)'],
    ['(fiction$)'],
    ['(s2j$)', '(smoke2jointz$)'],
    ['(ice$)'],
    ['(sfat$)'],
    ['(zhu$)'],
    ['(kirbykaze$)', '(kk$)'],
    ['(nintendude$)'],
    ['(macd$)'],
    ['(amsa$)'],
    ['(chillindude$)', '(chillindude829$)', '(chillin$)'],
    ['(javi$)'],
    ['(kels$)'],
    ['(wizzrobe$)', '(wizzy$)'],
    ['(the moon$)', '(la luna$)', '(moon$)'],
    ['(eddy mexico$)'],
    ['(chu dat$)', '(chudat$)'],
    ['(bladewise$)'],
    ['(abate$)'],
    ['(zer[o0]$)'],
    ['(larry lurr$)', '(larrylurr$)', '(DEHF$)'],
    ['(hugs$)', '(hugs86$)'],
    ['(duck$)'],
    ['(dj nintendo$)', '(djn$)'],
    ['(kalamazhu$)', '(kalamazhoo$)', '(kzhu$)'],
    ['(lord$)'],
    ['(cactuar$)', '(cactus$)'],
    ['(weon-x$)', '(weon x$)', '(weonx$)'],
    ['(darkrain$)'],
    ['(kage$)', '(kage the warrior$)'],
    ['(zanguzen$)'],
    ['(silentspect[er][re]$)', '(silent spect[er][re]$)'],
    ['(koreandj$)', '(korean dj$)', '(kdj$)'],
    ['(swiftbass$)', '(swift$)', '(gibson zero$)', '(gibsonzero$)'],
    ['(z[o0]s[o0]$)'],
    ['(raynex$)'],
    ['(darkatma$)', '(atma$)'],
    ['(porkchops$)'],
    ['(ib$)', '(i\.b\.$)'],
    ['(darc$)'],
    ['(swedish delight$)', '(swedish$)'],
    ['(okamibw$)', '(okami bw$)', '(okami$)'],
    ['(ken$)', '(sephiroth ken$)', '(sephirothken$)'],
    ['(vanz$)'],
    ['(excel zer[o0]$)', '(excelzero$)'],
    ['(darrell$)', '(darell$)', '(darrel$)'],
    ['(sl[o0]x$)', '(sl[o0]x\)$)'],
    ['(beer man$)', '(beer master$)', '(lambchops$)'],
    ['(s[o0]ft$)'],
    ['(fuzzyness$)'],
    ['(taf[o0]kints$)', '(taf[o0]$)'],
    ['(lil fumi$)', '(santi$)', '(santiago$)'],
    ['(dart$)', '(dart!$)'],
    ['(blea gelo$)', '(bleagelo$)'],
    ['(redd$)'],
    ['(hanky panky$)', '(hankypanky$)'],
    ['(remen$)'],
    ['(str[1i]cn[1iy]n[e3]$)', '(str[1i]c9$)', '(str[1i]c n[1iy]n[e3]$)', '(str[1i]c 9$)'],
    ['(cyrain$)'],
    ['(homemadewaffles$)', '(hmw$)', '(yung waff$)'],
    ['(pikachad$)', '(pika chad$)'],
    ['(ren[o0]$)'],
    ['(gahtzu$)', '(ghatzu$)'],
    ['(doh$)', '(darkness of heart$)'],
    ['(eggm$)'],
    ['(arc$)'],
    ['(t[o0]pe$)'],
    ['(drugged fox$)', '(druggedfox$)'],
    ['(gravy$)'],
    ['(tai$)'],
    ['(lucien$)'],
    ['(lord hdl$)', '(lordhdl$)'],
    ['(trail$)'],
    ['(scar$)'],
    ['(laudandus$)', '(laud[au][au]ndus$)', '(laduandus$)'],
    ['(t[o0]ph$)'],
    ['(alex19$)'],
    ['(c[o0]nn[o0]rthekid$)', '(c[o0]nn[o0]r$)', '(c[o0]nn[o0]r the kid$)'],
    ['([bj]izzarro flame$)', '([bj]izzarroflame$)', '([bj]izaro flame$)', '([bj]izzaro flame$)', '([bj]izarro flame$)'],
    ['(hyprid$)'],
    ['(a[zs]u[sz]a$)'],
    ['(m[o0]j[o0]$)'],
    ['(milkman$)', '(milk man$)'],
    ['(frootloop$)'],
    ['(esam$)'],
    # MIOM 2013 Rank Begins
    ['(wobbles$)', '(wobbles the phoenix$)'],
    ['(unknown522$)', '(unknown 522$)', '(ryan ford$)'],
    ['(taj$)'],
    ['(overtriforce$)', '(over$)', '(over triforce$)'],
    ['(dashizwiz$)', '(shiz$)', '(da shiz wiz$)'],
    ['(vwins$)'],
    ['(th[o0]rn$)'],
    ['(lovage$)'],
    ['(jman$)'],
    ['(gucci$)'],
    ['(blunted_object10$)', '(blunted_object$)', '(blunted object$)'],
    ['(bam$)'],
    ['(sung666$)', '(sung 666$)', '(sung$)'],
    ['(eggz$)'],
    ['(strawhat dahean$)', '(strawhat$)'],
    ['(vish$)'],
    ['(sion$)'],
    ['(phil$)'],
    ['(bob\$$)'],
    ['(kounotori$)'],
    ['(stab$)', '(victor abdul latif$)', '(stabbedbyahippie$)', '(stabbedbyanipple$)'],
    ['(g\$$)'],
    ['(vist$)'],
    ['(pkmvodka$)', '(pkm vodka$)']
    ],

    'New England' : [
    ['(sl[o0]x$)'],
    ['(koreandj$)', '(korean dj$)', '(kdj$)'],
    ['(swiftbass$)', '(swift$)', '(gibson zero$)', '(gibsonzero$)'],
    ['(z[o0]s[o0]$)'],
    ['(th[o0]rn$)'],
    ['(crush$)'],
    ['(mafia$)', '(irish mafia$)', '(slimjim$)', '(slim jim$)'], 
    ['(mdz$)', '(mattdotzeb$)', '(matt dot zeb$)'],
    ['(klap[s$]$)'],
    ['(tian$)'],
    ['(squible$)'],
    ['(kyupuff$)', '(kyu puff$)', '(plop$)', '(buffglutes92$)', '(the pleaup$)'],
    ['(rime$)'],
    ['(mr lemon$)', '(mr\. lemon$)'],
    ['(kaiju$)'],
    ['(dudutsai$)', '(tsai$)', '(stb$)'],
    ['(sora$)'],
    ['(hart$)'],
    ['(mr tuesday$)', '(mr\. tuesday$)'],
    ['(bigvegetabluntz$)', '(bvb$)', '(dylandude829$)'],
    ['(me[tl][tl]wing$)'], 
    ['(b[o0]lt$)', '(b[o0]wn$)'],
    ['(cheezpuff$)'],
    ['(r2dliu$)'],
    ['(kaza[am]m$)', '(kaza[am]mtheman$)'],
    ['(trademark$)'],
    ['(yedi$)'],
    ['(bugatti$)', '(mr bugatti$)', '(mr\. bugatti$)'],
    ['(ryucloud$)', '(ryu cloud$)'],
    ['(mizu$)'],
    ['(batsox$)'],
    ['(bonfire10$)', '(bonfire$)'],
    ['(trilok$)'],
    ['(kunai$)', '(wx$)', '(wxia$)'],
    ['(arc$)', '(arcnatural$)', '(arc natural$)'],
    ['(flexed$)'],
    ['(spiff$)'],
    ['(me[tl][tl]wing$)'],
    ['(vudoo$)'],
    ['(tichinde925$)', '(tichinde$)', '(master of setups$)'],
    ['(bugatti$)', '(colinsfuckboi$)', '(tpains producer$)'],
    ['(makari$)'],
    ['(young bone[sz] villain$)', '(yung bone[sz] villain$)', '(yungbone[sz]villain)', '(youngbone[sz]villain)'],
    ['(thechocolatelava$)', '(middleeastballz$)'],
    ['(tonic$)'],
    ['(broth chiler$)', '(broth chiller$)'],
    ['(hea7$)', '(areallyshittysheik$)'],
    ['(torsional strain$)', '(torsionalstrain$)'],
    ['(bonk$)', '(bonk cushy$)', '(bonkcushy$)', '(notable bonk$)'],
    ['(shkshk$)', '(shk shk)'],
    ['(snoweiner$)', '(snowweiner$)'],
    ['(stoc$)'],
    ['(wind$)'],
    ['(swissmiss$)', '(swiss miss$)'],
    ['(hackey$)'],
    ['(heropon$)', '(2dank$)'],
    ['(dis$)'],
    ['(edwin dexter$)', '(edwindexter$)'],
    ['(mizuki$)'],
    ['(corona$)'],
    ['(spooky ghost$)', '(spookyghost$)'],
    ['(spell$)'],
    ['(maso$)'],
    ['(jlo$)'],
    ['(coldo$)'],
    ['(nfreak$)'],
    ['(hazard$)'],
    ['(solar$)'],
    ['(pyro$)'],
    ['(bluntmaster$)', '(blunt master$)'],
    ['(para$)'],
    ['(racer$)', '(cashbags fatstackington$)', '(racer\$$)', '(racer.money$)', '(mr\. melon$)', '(mr melon$)'],
    ['(seaghost$)', '(sea ghost$)'],
    ['(fang$)'],
    ['(null$)'],
    ['(gtowntom$)', '(gtown tom)'],
    ['(barbie$)'],
    ['(red rice$)', '(redrice$)'],
    ['(doom$)'],
    ['(darc$)'],
    ['(rarik$)'],
    ['(guti$)'],
    ['(poobanans$)'],
    ['(zila$)'],
    ['(corona$)'],
    ['(uboa$)', '(greyface$)'],
    ['(lint$)'],
    ['(razz$)'],
    ['(blazingsparky$)', '(blazing sparky$)', '(blazing spark$)', '(blazingspark$)'],
    ['(zeo$)'],
    ['(connor$)']
    ],

    'NorCal' : [
    ['(shroomed$)'],
    ['(pewpewu$)', '(ppu$)', '(pewpewyou$)'],
    ['(sfat$)'],
    ['(silentspect[er][re]$)', '(silent spect[er][re]$)'],
    ['(darrell$)', '(darell$)', '(darrel$)'],
    ['(homemadewaffles$)', '(hmw$)', '(yung waff$)'],
    ['(lucien$)'],
    ['(scar$)'],
    ['(laudandus$)'],
    ['(t[o0]ph$)'],
    ['([bj]izzarro flame$)', '([bj]izzarroflame$)', '([bj]izaro flame$)', '([bj]izzaro flame$)', '([bj]izarro flame$)'],
    ['(hyprid$)'],
    ['(a[zs]u[sz]a$)'],
    ['(phil$)']
    ],

    'SoCal' : [
    ['(mang[o0]$)', '(c9mang[o0]$)'],
    ['(lucky$)'],
    ['(westballz$)'],
    ['(fly amanita$)'],
    ['(fiction$)'],
    ['(s2j$)', '(smoke2jointz$)'],
    ['(macd$)'],
    ['(eddy mexico$)'],
    ['(larry lurr$)', '(larrylurr$)', '(DEHF$)'],
    ['(hugs$)', '(hugs86$)'],
    ['(okamibw$)', '(okami bw$)', '(okami$)'],
    ['(ken$)', '(sephiroth ken$)', '(sephirothken$)', '(liquidken$)'],
    ['(taf[o0]kints$)', '(taf[o0]$)'],
    ['(lil fumi$)', '(santi$)', '(santiago$)'],
    ['(ren[o0]$)'],
    ['(alex19$)'],
    ['(c[o0]nn[o0]rthekid$)', '(c[o0]nn[o0]r$)', '(c[o0]nn[o0]r the kid$)'],
    ['([bj]izzarro flame$)', '([bj]izzarroflame$)', '([bj]izaro flame$)', '([bj]izzaro flame$)', '([bj]izarro flame$)'],
    ['(hyprid$)'],
    ['(lovage$)'],
    ['(sung666$)', '(sung 666$)', '(sung$)', '(sung475$)', '(sung 475$)'],
    ['(stab$)', '(victor abdul latif$)', '(stabbedbyahippie$)', '(stabbedbyanipple$)', '(matt$)'],
    ['(mikehaze$)', '(mike haze$)'],
    ['(kira$)'],
    ['(rofl$)'],
    ['(j666$)', '(j devil$)', '(jdevil$)'],
    ['(reason$)'],
    ['(a rookie$)', '(arookie$)'],
    ['(squid$)'],
    ['(jace$)'],
    ['(koopatroopa$)', '(koopatroopa895$)', '(koopa troopa$)', '(koopa troopa 895$)'],
    ['(captain faceroll$)', '(captainfaceroll$)', '(faceroll$)'],
    ['(psychomidget$)', '(psycho midget$)'],
    ['(jpegimage$)', '(jpeg image$)'],
    ['(sherigami$)', '(sherigam$)'],
    ['(mevan$)'],
    ['(coolhat$)', '(cool hat$)'],
    ['(peligro$)'],
    ['(dunk$)'],
    ['(dendypretendy$)', '(dendy$)', '(dendy pretendy)'],
    ['(khepri$)'],
    ['(mixx$)'],
    ['(sacasumoto$)'],
    ['(null$)'],
    ['(zeo$)'],
    ['(tonic$)']
    ],

    'North Carolina' : [
    ['(l[o0]zr$)'],
    ['(jwilli$)'],
    ['(ts3d$)'],
    ['(cope$)', '(ke$ha$)', '(sgt\. thunderfist md$)'],
    ['(wharve$)', '(warve$)'],
    ['(mining elf$)', '(elf$)'],
    ['(dembo$)', '(discoprof$)', '(d\'embaux$)', '(discovery professor dembo$)', '(d\'embeaux$)'],
    ['(tenbutts$)', '(ten butts$)'],
    ['(quetpie$)', '(andrew que$)', '(que t pie$)', '(quetpie forever$)'],
    ['(loudpackmatt$)', '(n$)', '(loud$)', '(loudpackmatt$)'],
    ['(tinkle$)', '(tinkl$)'],
    ['(catfish joe$)', '(joey bluntz$)'],
    ['(banjo$)', '(banjo d\. fingers$)'],
    ['(kchain\$$)', '(dr\. fingerdicks$)', '(dr\. fd$)'],
    ['(t raw$)', '(traw$)'],
    ['(@the_priceisnice$)', '(alanp$)'],
    ['(arundo$)', '(arumdo$)'],
    ['(caleb$)', '(oak town$)', '(not caleb$)', '(caliber$)'],
    ['(madz$)', '(maddie$)'],
    ['(niq$)'],
    ['(geezer$)'],
    ['(ezvega$)'],
    ['(salscat$)', '(salsacat$)', '(salsa cat$)'],
    ['(kun\$$)'],
    ['(byrd$)'],
    ['(\):)', '(:\()'],
    ['(cloudsquall$)']
    ]
    }

# Sanitized tags representing global top players.
sanitized_tags_dict = {
    'Global' : [
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
    'Connor',
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
    'Sung',
    'Eggz',
    'Strawhat Dahean',
    'Vish',
    'Sion',
    'Phil',
    'Bob$',
    'Kounotori',
    'Matt (Stab)',
    'G$',
    'Vist',
    'Pkmvodka'
    ],

    'New England' : [
    'Slox',
    'KoreanDJ',
    'Swift',
    'Zoso',
    'Thorn',
    'Crush',
    'Mafia',
    'MattDotZeb',
    'Klap$',
    'Tian',
    'Squible',
    'Kyu Puff',
    'Rime',
    'Mr. Lemon',
    'Kaiju',
    'Dudutsai',
    'Sora',
    'Hart',
    'Mr. Tuesday',
    'BVB',
    'Metlwing',
    'Bolt',
    'Cheezpuff',
    'R2DLiu',
    'Kazamm',
    'Trademark',
    'Yedi',
    'Bugatti',
    'RyuCloud',
    'MIZU',
    'BatSox',
    'Bonfire10',
    'Trilok',
    'Kunai',
    'Arc',
    'Flexed',
    'Spiff',
    'Metlwing',
    'Vudoo',
    'Tichinde',
    'Bugatti',
    'Makari',
    'Yung Bones Villain',
    'TheChocolateLava',
    'Tonic [New England]',
    'Broth Chiler',
    'Hea7',
    'Torsional Strain',
    'Bonk',
    'Shk Shk',
    'Snowweiner',
    'STOC',
    'Wind',
    'Swissmiss',
    'Hackey',
    'Heropon',
    'Dis',
    'Edwin Dexter',
    'Mizuki',
    'Corona',
    'Spooky Ghost',
    'Spell',
    'Maso',
    'JLo',
    'Coldo',
    'NFreak',
    'Hazard',
    'Solar',
    'Pyro',
    'Bluntmaster',
    'Para',
    'Racer',
    'Seaghost',
    'Fang',
    'Null [New England]',
    'Gtown_Tom',
    'Barbie',
    'Red Rice',
    'Doom',
    'Darc',
    'Rarik',
    'Guti',
    'Poobanans',
    'Zila',
    'Corona',
    'Uboa',
    'Lint',
    'Razz',
    'BlazingSparky',
    'Zeo [New England]',
    'Connor [New England]'
    ],

    'NorCal' : [
    'Shroomed',
    'PewPewU',
    'SFAT',
    'SilentSpectre',
    'Darrell',
    'HomeMadeWaffles',
    'Lucien',
    'Scar',
    'Laudandus',
    'Toph',
    'Bizzarro Flame',
    'Hyprid',
    'Azusa',
    'Phil'
    ],

    'SoCal' : [
    'Mango',
    'Lucky',
    'Westballz',
    'Fly Amanita',
    'Fiction',
    'S2J',
    'MacD',
    'Eddy Mexico',
    'Larry Lurr',
    'HugS',
    'OkamiBW',
    'Ken',
    'Tafokints',
    'Santiago',
    'Reno',
    'Alex19',
    'Connor [SoCal]',
    'Bizzarro Flame',
    'Hyprid',
    'Lovage',
    'Sung',
    'Matt (Stab)',
    'Mike Haze',
    'Kira',
    'Rofl',
    'J666',
    'Reason',
    'A Rookie',
    'Squid',
    'Jace',
    'KoopaTroopa',
    'Captain Faceroll',
    'PsychoMidget',
    'JPeGImage',
    'Sherigami',
    'Mevan',
    'Coolhat',
    'Peligro',
    'Dunk',
    'DendyPretendy',
    'Khepri',
    'Mixx',
    'SacaSuMoto',
    'Null [SoCal]',
    'Zeo [SoCal]',
    'Tonic [SoCal]'
    ],

    'North Carolina' : [
    'LoZR',
    'Jwilli',
    'TS3D',
    'Ke$ha',
    'Wharve',
    'Mining Elf',
    'Dembo',
    'tenbutts',
    'QueTPie',
    'Loudpackmatt',
    'Tinkle',
    'Catfish Joe',
    'Banjo',
    'KChain$',
    'T Raw',
    '@The_PriceisNICE',
    'Arundo',
    'Caleb [North Carolina]',
    'Madz',
    'Niq',
    'Geezer',
    'EZVega',
    'Salsacat',
    'Kun$',
    'Byrd',
    '):',
    'Cloudsquall'
    ]
    }

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

# Identical to sanitize_tag, but returns list of matching regex expressions instead of returning the first one
def sanitize_tag_multiple(tag, regex_list, sanitized_list):
  tag_list = []
  for i in range(len(regex_list)):
    if regex_list[i].match(tag):
      tag_list.append(sanitized_list[i])
  return tag 

# Takes player_raw_regex_dict[region] as a parameter through map, meaning that each index is one list inside the list of regex expressions in player_raw_regex_dict['Global$)'].
def add_prefixes(regex_list):
  wildcard = '.*'
  sep = '[|_.`\' ]'
  # suffix = '$)'
  prefix = wildcard + sep
  prefix_list = []
   
  inner_list = []
  for regex in regex_list:
    # 4 combinations
    inner_list.append(regex) 
    # inner_list.append(regex + '\)' + suffix) 
    inner_list.append(prefix + regex)
    # inner_list.append(prefix + regex + ')' + suffix) 

  joined_regex = '|'.join(inner_list)
  prefix_list.append(joined_regex)
  return joined_regex

# if region==None or region==Global:
  # prefixed_player_regex_list = map(add_prefixes, player_raw_regex_dict['Global$)'])
  # player_regex_list = 
# else:
  # if region in Regex_list_dict:
    # prefixed_player_regex_list = map(add_prefixes, player_raw_regex_dict['Global$)'])
    # player_regex_list = map(compile_case_i_re, player_raw_regex_dict['Global$)'])

# Convert all lists in player_raw_regex_dict to a version with regular expression prefixes wildcard and sep added and suffix, then compile both list to all lowercase tags
player_regex_dict = defaultdict(str)
for region_name in player_raw_regex_dict:
  # print "-----REGION_NAME", region_name 
  player_regex_dict[region_name] = map(add_prefixes, player_raw_regex_dict[region_name])
  # print "-----PREFIXED_REGEX_DICT", player_regex_dict[region_name]
  player_regex_dict[region_name] = map(compile_case_i_re, player_regex_dict[region_name])
  # print "-----LOWERCASE", player_regex_dict
  # print '\n'
# print "----- PLAYER_REGEX_DICT", player_regex_dict

# Combine region-separated values of player_regex_dict for a truly global list
# Combine region-separated values of sanitized_tags_dict for a truly comprehensive list
full_regex_list = []
full_sanitized_list = []
for region in player_regex_dict:
  full_regex_list += player_regex_dict[region]
  full_sanitized_list += sanitized_tags_dict[region]
# print "-----FULL_REGEX_LIST", full_regex_list
# print "-----FULL_SANITIZED_LIST", full_sanitized_list

# Wrapper for sanitize_tag.
def check_and_sanitize_tag(tag, *args): #region is optional parameter
  # if region is included in parameter, use region list
  if len(args)==1 and args[0] is not None:
    region_name = args[0]
    if region_name in player_raw_regex_dict and region_name in sanitized_tags_dict:
      return sanitize_tag(tag, player_regex_dict[region_name], sanitized_tags_dict[region_name]) 
  elif len(args)==0 or args[0] is None:
    region_name = "Global"
    return sanitize_tag(tag, full_regex_list, full_sanitized_list)

# Identical to check_and_sanitize_tag, but returns list of all matches
def check_and_sanitize_tag_multiple(tag, *args):
  # if region is included in parameter, use region list
  if len(args)==1 and args[0] is not None:
    region_name = args[0]
    if region_name in player_raw_regex_dict and region_name in sanitized_tags_dict:
      return sanitize_tag_multiple(tag, player_regex_dict[region_name], sanitized_tags_dict[region_name]) 
  elif len(args)==0 or args[0] is None:
    region_name = "Global"
    return sanitize_tag_multiple(tag, full_regex_list, full_sanitized_list)

# Function that checks the lengths of the raw regex dict and sanitized tags dict, and prints each index together for comparison
def debug_regex_lists(*args):
# if region is included in parameter, use region list
  if len(args)==1 and args[0] is not None:
    region_name = args[0]
    print "Regex length: ", len(player_raw_regex_dict[region_name])
    print "Sanitized length: ", len(sanitized_tags_dict[region_name])
    for i in range(len(player_regex_dict[region_name])):
      print player_raw_regex_dict[region_name][i], sanitized_tags_dict[region_name][i]
  elif len(args)==0 or args[0] is None:
    region_name = "Global"
    print "Regex length: ", len(player_raw_regex_dict['Global'])
    print "Sanitized length: ", len(sanitized_tags_dict['Global'])
    for i in range(len(player_regex_dict['Global'])):
      print player_raw_regex_dict['Global'][i], sanitized_tags_dict['Global'][i]

