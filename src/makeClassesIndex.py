#!/usr/bin/env python3
# -*- coding: utf-8 -*-

path = pathlib.Path(__file__).parent.absolute() 

classes_dict = {}
functions = []

with open(str(path) + "/src/basicClasses.txt", "r") as f:
  lines = f.readlines()
  for l in lines:
    l = l.strip()
    functions.append(l)
    new_string = l[0].lower()
    for x in l[1:]:
      if x.islower():
        new_string += x
      else:
        new_string += (" " + x.lower())
    words = new_string.split()
    first_word = words[0].lower()
    if first_word in classes_dict:
      if new_string in classes_dict[first_word]:
        if l in classes_dict[first_word][new_string]:
          pass
        else:
          classes_dict[first_word][new_string] = classes_dict[first_word][new_string] + [l]
      else:
        classes_dict[first_word][new_string] = [l]
    else:
      classes_dict[first_word] = {new_string: [l]} # + "s"


del classes_dict['n']['n c a a team season']
classes_dict['NCAA'] = {'NCAA team season' : ['NCAATeamSeason']}
classes_dict['organizations'] = {'organizations' : ['Company']}
classes_dict['organisation'] = {'organisation' : ['Company']}
classes_dict['organisations'] = {'organisations' : ['Company']}
del classes_dict['non']['non h y p h e n profit organisation']
classes_dict['nonprofit'] = {'nonprofit organisation' : ['Non-ProfitOrganisation'], 'nonprofit organisations' : ['Non-ProfitOrganisation']}
classes_dict['non-profit'] = {'non-profit organisation' : ['Non-ProfitOrganisation'], 'non-profit organisations' : ['Non-ProfitOrganisation']}
del classes_dict['t']['t v show']
del classes_dict['womens']['womens tennis association tournament']
classes_dict['women\'s'] = {'women\'s tennis association tournament': ['WomensTennisAssociationTournament']}
classes_dict["grand"] = {'grand prix': ['GrandPrix'], 'grand prixes': ['GrandPrix']}
classes_dict["f"] = {'f1 racer': ['FormulaOneRacer']}
classes_dict["color"] = {'color': ['Colour']}
classes_dict["colors"] = {'colors': ['Colour']}
classes_dict["comic"]["comic character"] = ['ComicsCharacter']
classes_dict["comic"]["comic characters"] = ['ComicsCharacter']
classes_dict["automobile"]["automobile engine"] = ['AutomobileEngine']
classes_dict["automobile"]["automobile engines"] = ['AutomobileEngine']
classes_dict["musical"]["musical artist"] = ['MusicalArtist']
classes_dict["musical"]["musical artists"] = ['MusicalArtist']
classes_dict["soccer"]["soccer club season"] = ['SoccerClubSeason']
classes_dict["soccer"]["soccer club seasons"] = ['SoccerClubSeason']
classes_dict["race"]["race horse"] = ['RaceHorse']
classes_dict["race"]["race horses"] = ['RaceHorse']
classes_dict["sports"]["sports manager"] = ['SportsManager']
classes_dict["sports"]["sports managers"] = ['SportsManager']
classes_dict["radio"] = {'radio programs': ['RadioProgram'], 'radio station': ['RadioStation'], 'radio host': ['RadioHost'], 'radio stations': ['RadioStation'], 'radio': ['RadioStation'], 'radio program': ['RadioProgram'], 'radio hosts': ['RadioHost'], 'radio programme': ['RadioProgram'], 'radio programmes': ['RadioProgram']}
classes_dict["television"] = {'television host': ['TelevisionHost'], 'television programs': ['TelevisionShow'], 'television seasons': ['TelevisionSeason'], 'television stations': ['TelevisionStation'], 'television series': ['TelevisionShow'], 'television episodes': ['TelevisionEpisode'], 'television hosts': ['TelevisionHost'], 'television program': ['TelevisionShow'], 'television shows': ['TelevisionShow'], 'television show': ['TelevisionShow'], 'television season': ['TelevisionSeason'], 'television episode': ['TelevisionEpisode'], 'television station': ['TelevisionStation'], 'television programmes': ['TelevisionShow'], 'television programme': ['TelevisionShow']}
classes_dict["tv"] = {'tv host': ['TelevisionHost'], 'tv programs': ['TelevisionShow'], 'tv seasons': ['TelevisionSeason'], 'tv stations': ['TelevisionStation'], 'tv series': ['TelevisionShow'], 'tv episodes': ['TelevisionEpisode'], 'tv hosts': ['TelevisionHost'], 'tv program': ['TelevisionShow'], 'tv shows': ['TelevisionShow'], 'tv show': ['TelevisionShow'], 'tv season': ['TelevisionSeason'], 'tv episode': ['TelevisionEpisode'], 'tv station': ['TelevisionStation'], 'tv programmes': ['TelevisionShow'], 'tv programme': ['TelevisionShow']}

with open(str(path) + "/src/classesPl.txt", "r") as f:
  lines = list(f)
  lines = lines[0].split('\r')
  i = 0
  for l in lines:
    l = l.strip()
    words = l.split()
    first_word = words[0].lower()
    if first_word in classes_dict:
      if l in classes_dict[first_word]:
        if functions[i] in classes_dict[first_word][l]:
          i += 1
        else:
          classes_dict[first_word][l] = classes_dict[first_word][l] + [functions[i]]
          i += 1
      else:
        classes_dict[first_word][l] = [functions[i]]
        i += 1
    else:
      classes_dict[first_word] = {l: [functions[i]]}
      i += 1

with open(str(path) + "/src/class_corr.py", "r") as f:
  lines = f.readlines()
  for l in lines:
    l = l.strip()
    matches = re.search('"(.*?)" : \[(.*?)\],\\\\$', l)
    if matches == None:
      pass
    else:
      match1 = matches.group(1)
      match2 = matches.group(2)
      new_string = match1[0].lower()
      for x in match1[1:]:
        if x.islower():
          new_string += x
        else:
          new_string += (" " + x.lower())
      words = new_string.split()
      first_word = words[0].lower()
      values = match2.replace("\"", "").split(", ")
      if first_word in classes_dict:
        if new_string in classes_dict[first_word]:
          classes_dict[first_word][new_string] = values
      else:
        classes_dict[first_word] = {new_string : values}

with open(str(path) + "/src/class_corr.py", "r") as f:
  lines = f.readlines()
  for l in lines:
    l = l.strip()
    matches = re.search('"(.*?)" : \[(.*?)\],\\\\$', l)
    if matches == None:
      pass
    else:
      match1 = matches.group(1)
      match2 = matches.group(2)
      new_string = match1[0].lower()
      for x in match1[1:]:
        if x.islower():
          new_string += x
        else:
          new_string += (" " + x.lower())
      new_string = new_string + "s"
      words = new_string.split()
      first_word = words[0].lower()
      values = match2.replace("\"", "").split(", ")
      if first_word in classes_dict:
        if new_string in classes_dict[first_word]:
          classes_dict[first_word][new_string] = values
      else:
        classes_dict[first_word] = {new_string : values}
