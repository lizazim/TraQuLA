#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def make_full_link(lst):
  new_lst = []
  for l in lst:
    if l.startswith("http://dbpedia.org/resource/"):
      new_lst.append(l)
    else:
      new_lst.append("http://dbpedia.org/resource/" + l)
  return new_lst

def make_short_link(lst):
  new_lst = []
  for l in lst:
    if l.startswith("http://dbpedia.org/resource/"):
      new_lst.append(l[28:])
    else:
      new_lst.append(l)
  return new_lst
  
############################

def is_number(s):
  try:
    float(s)
    return True
  except ValueError:
    pass
  try:
    unicodedata.numeric(s)
    return True
  except (TypeError, ValueError):
    pass
  return False

############################

alpha = list(string.ascii_lowercase)

ind_names = []

for l1 in alpha:
  for l2 in alpha:
    ind_name = l1 + l2
    ind_names.append(ind_name)

def flat_list(l):
  return [item for sublist in l for item in sublist]
  
def find_intersecting_elements(elements):
  intersect = False
  i = 0
  while intersect == False and i < len(elements):
    current_element = elements[i]
    right_elements = elements[i + 1:]
    if right_elements == []:
      pass
    else:
      if isinstance(current_element[1], list): # entities
        text_words1 = current_element[1]
      else:
        text_words1 = current_element[1][0] # properties and classes
      indexes_taken1 = range(current_element[0], current_element[0] + len(text_words1))
      for x in right_elements:
        if isinstance(x[1], list): # entities
          text_words2 = x[1]
        else:
          text_words2 = x[1][0] # properties and classes
        indexes_taken2 = range(x[0], x[0] + len(text_words2))
        if list(set(indexes_taken1) & set(indexes_taken2)) != []:
          intersect = True
        else:
          pass
    i += 1
  return intersect

def check_capitalisation(word1, word2):
  upper = False
  for (x, y) in zip(word1, word2):
    if x == y and x.isupper() == True:
      upper = True
    elif x != y:
      return False
    else:
      pass
  return upper

def rank_pairs(pairs, matches):
  for (a,b) in pairs:
    if a[-1].isalpha() == False and is_number(a[-1]) == False and is_number(a) == False and len(a) > 1: # this will also include "É", etc.
      a = a[:-1]
    if b[-1].isalpha() == False and is_number(b[-1]) == False and is_number(b) == False and len(b) > 1: # this will also include "É", etc.
      b = b[:-1]
    a_lower = a.lower()
    b_lower = b.lower()
    if a_lower == b_lower and a_lower in ["a", "the"]:
      matches += 0.5
    elif a_lower == b_lower:
      if check_capitalisation(a, b) == True:
        matches += 2
      else:
        matches += 1
    elif a_lower + "s" == b_lower or a_lower + "es" == b_lower or a_lower[:-1] + "ies" == b_lower or a_lower[:-1] == b_lower or \
        (len(a_lower) > 3 and a_lower[:-3] + "y" == b_lower) or b_lower + "s" == a_lower or b_lower + "es" == a_lower or \
        b_lower[:-1] + "ies" == a_lower or b_lower[:-1] == a_lower or (len(b_lower) > 3 and b_lower[:-3] + "y" == a_lower) or fuzz.ratio(a_lower, b_lower) > 90:
      matches += 0.5
  return matches

def arrange_by_matches(combinations, entities, properties, classes, words):
  new_combinations = []
  for c in combinations:
    has_bracket = False # entities without brackets are preferred if there are no brackets in the question ('Linda Hogan' is better than 'Linda Hogan (television personality)')
    matches = 0
    for element in c:
      if isinstance(element[1], list): # entities
        text_words = element[1]
        if "(" in " ".join(text_words):
          has_bracket = True
      else:
        text_words = element[1][0] # properties and classes
      e_str_without_punctuation = (str(" ".join(text_words))) #.translate(None, string.punctuation)
      e_lst_without_punctuation = e_str_without_punctuation.split()
      right_words = words[element[0]:]
      right_words_str_without_punctuation = str(" ".join(right_words)) #.translate(None, string.punctuation)
      right_words_lst_without_punctuation = right_words_str_without_punctuation.split()[:len(e_lst_without_punctuation)]
      pairs = zip(e_lst_without_punctuation, right_words_lst_without_punctuation)
      matches = rank_pairs(pairs, matches)
    if has_bracket == True and "(" not in " ".join(words):
      matches -= 0.25
    new_combinations.append((c, matches))
  new_combinations.sort(key = lambda x: x[1], reverse = True)
  new_combinations = check_neighbouring_class_and_entity(new_combinations, entities, classes)
  new_combinations = check_neighbouring_properties_ranked(new_combinations, properties, words)
  if new_combinations == []:
    return new_combinations
  else:
    top_score = new_combinations[0][1]
    top_score_parses = []
    other = []
    for x in new_combinations:
      if x[1] == top_score:
        top_score_parses.append(x)
      else:
        other.append(x)
    top_score_parses.sort(key = lambda x: len(x[0]))
    new_combinations = [x[0] for x in top_score_parses + other]
    return new_combinations

def find_second_prop(parse, words, props):
  indexes_taken = []
  for x in parse:
    if isinstance(x[1], list): # entities
      text_words = x[1]
    else:
      text_words = x[1][0] # properties and classes
    x_indexes_taken = range(x[0], x[0] + len(text_words))
    indexes_taken += x_indexes_taken
  possible_second_prop = []
  for x in props:
    x_indexes_taken = range(x[0], x[0] + len(x[1][0]))
    if list(set(indexes_taken) & set(x_indexes_taken)) == []: # if property does not intersect with elements found
      possible_second_prop.append(x)
  possible_second_prop.sort(key = lambda x: len(x[1][0]), reverse = True)
  if possible_second_prop != []:
    parse.append(possible_second_prop[0])
    return parse
  else:
    return parse

def find_second_ent(parse, words, ents):
  indexes_taken = []
  entity_indexes_taken = []
  for x in parse:
    if isinstance(x[1], list): # entities
      text_words = x[1]
      entity_indexes_taken = range(x[0], x[0] + len(text_words))
    else:
      text_words = x[1][0] # properties and classes
    x_indexes_taken = range(x[0], x[0] + len(text_words))
    indexes_taken += x_indexes_taken
  possible_second_ent = []
  for x in ents:
    x_indexes_taken = range(x[0], x[0] + len(x[1]))
    x_index_start = x_indexes_taken[0]
    if x_index_start < entity_indexes_taken[0]:
      if list(set(indexes_taken) & set(x_indexes_taken)) == [] and entity_indexes_taken[0] - x_indexes_taken[-1] > 1: # 2 and x[0] != 0: # if property does not intersect with elements found
        possible_second_ent.append(x)
    else:
      if list(set(indexes_taken) & set(x_indexes_taken)) == [] and x_index_start - entity_indexes_taken[-1] > 1: # 2 and x[0] != 0:
        possible_second_ent.append(x)
  if possible_second_ent != []:
    ranked_possible_second_ent = []
    for ent in possible_second_ent:
      e_words = ent[1]
      matches = 0
      if "(" in " ".join(e_words):
        has_bracket = True
      else:
        has_bracket = False # entities without brackets are preferred if there are no brackets in the question ('Linda Hogan' is better than 'Linda Hogan (television personality)')
      text_words = words[ent[0]:][:len(e_words)]
      pairs = zip(e_words, text_words)
      matches = rank_pairs(pairs, matches)
      if has_bracket == True and "(" not in " ".join(words):
        matches -= 0.25
      ranked_possible_second_ent.append((ent, matches))
    ranked_possible_second_ent.sort(key = lambda x: x[1], reverse = True)
    parse.append(ranked_possible_second_ent[0][0])
    return parse
  else:
    return parse

############################

def props_search_with_split(prop, ent, dir, record_name, format):
  props_search = index_request(format, dir, record_name, ent)
  if props_search == []:
    props_search = index_request(format, dir, record_name, ent + "_SPLITSUBJECT1")
    if props_search != []:
      x = 2
      new_cands = index_request(format, dir, record_name, ent + "_SPLITSUBJECT" + str(x))
      props_search += new_cands
      while new_cands != []:
        x += 1
        new_cands = index_request(format, dir, record_name, ent + "_SPLITSUBJECT" + str(x))
        props_search += new_cands
      return props_search
    else:
      return []
  else:
    return props_search

def interpret_prop_results(prop_str):
  return [x.split(" ", 1) for x in re.split('\', \'|\', "|", "|", \'', prop_str[1:-1])]
  
def strict_search_prop_in_index(prop, ent, dir, record_name, format):
  props_search = props_search_with_split(prop, ent, dir, record_name, format)
  if props_search == []:
    return ([], [])
  else:
    found_props_minus_brackets = [x.decode('utf-8')[1:-1] for x in props_search if len(x) > 2]
    found_props = interpret_prop_results(", ".join(found_props_minus_brackets))
    results = []
    for x in found_props:
      if len(x) == 1:
        pass
      else:
        [p, v] = x
        if p == prop:
          results.append(v)
    if results == []:
      return ([], found_props)
    else:
      if dir.startswith("propertiesIndexReverse"):
        reverse = True
      else:
        reverse = False
      return ((prop, reverse, results), found_props)

def shorten_prop(prop):
  if prop.startswith("property/") or prop.startswith("ontology/"):
    prop = prop[9:]
  else:
    prop = prop[28:]
  return prop

def normalise_prop_for_sparql(prop):
  if prop.startswith("http://dbpedia.org/"):
    prop = prop[19:]
  return prop
        
def non_strict_search_prop_in_index(prop, ent, reverse, found_props):
  if found_props == []:
    return []
  else:
    results = []
    for [p1, v1] in found_props:
      if fuzz.ratio(shorten_prop(p1), shorten_prop(prop)) > 90: # without "property/" and "ontology/"
        results.append(v1)
        for [p2, v2] in found_props:
          if p1 == p2 and v2 not in results:
            results.append(v2)
        if results != []:
          return (p1, reverse, results)
      results = []
      prop_words = re.findall('[A-Z][^A-Z]*', capitalise_first(shorten_prop(prop)))
      prop_words_minus_stop_words = [x.lower() for x in prop_words if x.lower() not in stop_words]
      p1_words = re.findall('[A-Z][^A-Z]*', capitalise_first(shorten_prop(p1)))
      p1_words = [x.lower() for x in p1_words]
      for w in prop_words_minus_stop_words:
        if w in p1_words or w + "s" in p1_words or w + "es" in p1_words or w[:-1] + "ies" in p1_words or w[:-1] in p1_words or (len(w) > 3 and w[:-3] + "y" in p1_words):
          results.append(v1)
          for [p2, v2] in found_props:
            if p1 == p2 and v2 not in results:
              results.append(v2)
          if results != []:
            return (p1, reverse, results)
    if results == []:
      return []

def all_non_strict_props(prop, ent, reverse, found_props):
  if found_props == []:
    return []
  else:
    all_results = []
    for [p1, v1] in found_props:
      results_for_prop = []
      if fuzz.ratio(shorten_prop(p1), shorten_prop(prop)) > 90: # without "property/" and "ontology/"
        results_for_prop.append(v1)
        for [p2, v2] in found_props:
          if p1 == p2 and v2 not in results_for_prop:
            results_for_prop.append(v2)
        if results_for_prop != []:
          all_results.append((p1, reverse, results_for_prop))
      prop_words = re.findall('[A-Z][^A-Z]*', capitalise_first(shorten_prop(prop)))
      prop_words_minus_stop_words = [x.lower() for x in prop_words if x.lower() not in stop_words]
      p1_words = re.findall('[A-Z][^A-Z]*', capitalise_first(shorten_prop(p1)))
      p1_words = [x.lower() for x in p1_words]
      for w in prop_words_minus_stop_words:
        if w in p1_words or w + "s" in p1_words or w + "es" in p1_words or w[:-1] + "ies" in p1_words or w[:-1] in p1_words or (len(w) > 3 and w[:-3] + "y" in p1_words):
          results_for_prop.append(v1)
          for [p2, v2] in found_props:
            if p1 == p2 and v2 not in results_for_prop:
              results_for_prop.append(v2)
          if results_for_prop != []:
            all_results.append((p1, reverse, results_for_prop))
    return all_results

############################

def interpret_disamb_results(lst):
  if lst == []:
    return []
  else: 
    return re.split('\', \'|\', "|", "|", \'', lst[0].decode('utf-8')[2:-2])
  
def check_redirect_or_disamb(e, main_folder):
  if len(e) < 2:
    folder = "other"
  else:
    first_two = e.lower()[:2]
    if first_two not in ind_names:
      folder = "other"
    else:
      folder = first_two
  return index_request("#value", main_folder + folder, "subject", e)

def remove_duplicates_preserve_order(seq):
  seen = set()
  seen_add = seen.add
  return [x for x in seq if not (x in seen or seen_add(x))]

def find_ents_with_brackets(e, entities):
  e_without_brackets = re.sub(r'_\([^)]*\)', '', e)
  found = []
  for ent in entities:
    link = "_".join(ent[1])
    ent_without_brackets = re.sub(r'_\([^)]*\)', '', link)
    if ent_without_brackets == e_without_brackets:
      found.append(link)
  return found

def alternative_ents_from_parse(e, ent_index, entities):
  len_e = len(e.split('_'))
  if len_e > 1:
    same_index_ents = [x for x in entities if x[0] == ent_index and len(x[1]) > 1]
  else:
    same_index_ents = [x for x in entities if x[0] == ent_index]
  results = []
  for x in same_index_ents:
    ent = "_".join(x[1])
    results += check_redirects_and_disambs(ent, entities)
  return results

def check_redirects_and_disambs(e, entities):
  results = []
  redirect = []
  redirect = check_redirect_or_disamb(e, "redirectsindex/")
  if redirect == []:
    ent_lst = [e]
    disamb_request = e
  else:
    ent_lst = redirect
    disamb_request = redirect[0]
  if isinstance(disamb_request, (bytes, bytearray)):
    disamb_request = disamb_request.decode('utf-8')
  disambiguation1 = interpret_disamb_results(check_redirect_or_disamb(disamb_request, "disambiguations/"))
  disambiguation2 = interpret_disamb_results(check_redirect_or_disamb(disamb_request + "_(disambiguation)", "disambiguations/"))
  ents_with_brackets = find_ents_with_brackets(e, entities)
  ent_lst += (disambiguation1 + disambiguation2 + ents_with_brackets)
  results += remove_duplicates_preserve_order(ent_lst)
  results = remove_duplicates_preserve_order(results)
  if redirect != []:
    results.remove(e)
  return results

def check_famous_shortened_forms(e):
  if e in ["The_States", "The_states", "US", "us", "Us"]:
    return ["United_States"]
  elif e in ["The_UK", "UK", "uk", "Uk"]:
    return ["United_Kingdom"]
  else:
    return []
    
def make_entity_uris(e, ent_index, entities):
  famous_shortened_forms = check_famous_shortened_forms(e)
  redirects_and_disambs = check_redirects_and_disambs(e, entities)
  alternative_ents = alternative_ents_from_parse(e, ent_index, entities)
  result = remove_duplicates_preserve_order(famous_shortened_forms + redirects_and_disambs + alternative_ents)
  new_result = []
  for x in result:
    if isinstance(x, (bytes, bytearray)):
      new_result.append(x.decode('utf-8'))
    else:
        new_result.append(x)
  return remove_duplicates_preserve_order(new_result)

############################

years = ['1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977', '1978', '1979', \
         '1980', '1981', '1982', '1983', '1984', '1985', '1986', '1987', '1988', '1989', \
         '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', \
         '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', \
         '2010', '2011', '2012', '2013', '2014', '2015', '2016']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
alpha_pairs = [a + b for (a, b) in list(itertools.product(*[alpha, alpha]))]

def find_entity_folder(entity):
  if isinstance(entity, (bytes, bytearray)):
    entity = entity.decode('utf-8')
  entity = entity.lower()
  if len(entity) > 3 and entity[:4] in years:
    folder = entity[:4]
  elif len(entity) > 1 and entity[:2].lower() in alpha_pairs:
    folder = entity[:2]
  elif entity[0].lower() in alpha:
    folder = entity[0] + "_other"
  elif entity[0] in numbers:
    folder = entity[0]
  else:
    folder = "other"
  return folder
  
def find_direct_prop_folder(entity):
  return "propertiesindex/" + find_entity_folder(entity)

def find_reverse_prop_folder(entity):
  return "propertiesIndexReverse/" + find_entity_folder(entity)
  
def find_instance_type_folder(entity):
  return "instanceTypes/" + find_entity_folder(entity)
  
############################

def find_all_prop_matches(props, i_prop, entity, props_index, words):
  prop = props[i_prop]
  if prop.endswith("_O"):
    full_prop = "ontology/" + prop[:-2]
  else:
    full_prop = "property/" + prop[:-2]
  direct_folder = find_direct_prop_folder(entity)
  reverse_folder = find_reverse_prop_folder(entity)
  all_prop_matches = []
  if (props_index != 0 and words[props_index - 1].lower() in ["one", "whose", "has", "have", "had", "having", "with"]) or (props_index >= 1 and words[props_index - 2].lower() in ["one", "whose", "has", "have", "had", "having", "with"]) or words[props_index].lower().endswith("'s") or ((len(words) > props_index + 1) and words[props_index + 1].lower().endswith("'s")) or ((len(words) > props_index + 2) and words[props_index + 2].lower().endswith("'s")):
    (prop_matches, ontology_reverse_props) = strict_search_prop_in_index(full_prop, entity, reverse_folder, "subject", "#propval")
    if prop_matches != []:
      all_prop_matches.append(prop_matches)
    (prop_matches, ontology_reverse_props) = strict_search_prop_in_index(full_prop, entity, reverse_folder, "subject", "#propval")
    if prop_matches != []:
      all_prop_matches.append(prop_matches)
  else:
    (prop_matches, ontology_props) = strict_search_prop_in_index(full_prop, entity, direct_folder, "subject", "#propval")
    if prop_matches != []:
      all_prop_matches.append(prop_matches)
    (prop_matches, ontology_reverse_props) = strict_search_prop_in_index(full_prop, entity, reverse_folder, "subject", "#propval")
    if prop_matches != []:
      all_prop_matches.append(prop_matches)
  return all_prop_matches
  
def find_prop_matches(props, i_prop, entity, props_index, words):
  prop = props[i_prop]
  if prop.endswith("_O"):
    full_prop = "ontology/" + prop[:-2]
  else:
    full_prop = "property/" + prop[:-2]
  direct_folder = find_direct_prop_folder(entity)
  reverse_folder = find_reverse_prop_folder(entity)
  prop_matches = []
  if (props_index != 0 and words[props_index - 1].lower() in ["one", "whose", "has", "have", "had", "having", "with"]) or (props_index >= 1 and words[props_index - 2].lower() in ["one", "whose", "has", "have", "had", "having", "with"]) or words[props_index].lower().endswith("'s") or ((len(words) > props_index + 1) and words[props_index + 1].lower().endswith("'s")) or ((len(words) > props_index + 2) and words[props_index + 2].lower().endswith("'s")):
    (prop_matches, ontology_reverse_props) = strict_search_prop_in_index(full_prop, entity, reverse_folder, "subject", "#propval")
    if prop_matches == []:
      prop_matches = non_strict_search_prop_in_index(full_prop, entity, True, ontology_reverse_props)
      if prop_matches == []:
        (prop_matches, ontology_props) = strict_search_prop_in_index(full_prop, entity, direct_folder, "subject", "#propval")
        if prop_matches == []:
          prop_matches = non_strict_search_prop_in_index(full_prop, entity, False, ontology_props)
  else:
    (prop_matches, ontology_props) = strict_search_prop_in_index(full_prop, entity, direct_folder, "subject", "#propval")
    if prop_matches == []:
      prop_matches = non_strict_search_prop_in_index(full_prop, entity, False, ontology_props)
      if prop_matches == []:
        (prop_matches, ontology_reverse_props) = strict_search_prop_in_index(full_prop, entity, reverse_folder, "subject", "#propval")
        if prop_matches == []:
          prop_matches = non_strict_search_prop_in_index(full_prop, entity, True, ontology_reverse_props)
  return prop_matches

def find_prop_matches_strictly(props, i_prop, entity, props_index, words):
  prop = props[i_prop]
  if prop.endswith("_O"):
    full_prop = "ontology/" + prop[:-2]
  else:
    full_prop = "property/" + prop[:-2]
  direct_folder = find_direct_prop_folder(entity)
  reverse_folder = find_reverse_prop_folder(entity)
  prop_matches = []
  if (props_index != 0 and words[props_index - 1].lower() in ["one", "whose", "has", "have", "had", "having", "with"]) or (props_index >= 1 and words[props_index - 2].lower() in ["one", "whose", "has", "have", "had", "having", "with"]) or words[props_index].lower().endswith("'s") or ((len(words) > props_index + 1) and words[props_index + 1].lower().endswith("'s")) or ((len(words) > props_index + 2) and words[props_index + 2].lower().endswith("'s")):
    (prop_matches, ontology_reverse_props) = strict_search_prop_in_index(full_prop, entity, reverse_folder, "subject", "#propval")
    if prop_matches == []:
      (prop_matches, ontology_props) = strict_search_prop_in_index(full_prop, entity, direct_folder, "subject", "#propval")
  else:
    (prop_matches, ontology_props) = strict_search_prop_in_index(full_prop, entity, direct_folder, "subject", "#propval")
    if prop_matches == []:
      (prop_matches, ontology_reverse_props) = strict_search_prop_in_index(full_prop, entity, reverse_folder, "subject", "#propval")
  return prop_matches
  
def find_prop_matches_direct(props, i_prop, entity, props_index, words):
  prop = props[i_prop]
  if prop.endswith("_O"):
    full_prop = "ontology/" + prop[:-2]
  else:
    full_prop = "property/" + prop[:-2]
  direct_folder = find_direct_prop_folder(entity)
  prop_matches = []
  (prop_matches, ontology_props) = strict_search_prop_in_index(full_prop, entity, direct_folder, "subject", "#propval")
  if prop_matches == []:
    prop_matches = non_strict_search_prop_in_index(full_prop, entity, False, ontology_props)
  return prop_matches

def find_prop_matches_reverse(props, i_prop, entity, props_index, words):
  prop = props[i_prop]
  if prop.endswith("_O"):
    full_prop = "ontology/" + prop[:-2]
  else:
    full_prop = "property/" + prop[:-2]
  reverse_folder = find_reverse_prop_folder(entity)
  prop_matches = []
  (prop_matches, ontology_reverse_props) = strict_search_prop_in_index(full_prop, entity, reverse_folder, "subject", "#propval")
  if prop_matches == []:
    prop_matches = non_strict_search_prop_in_index(full_prop, entity, True, ontology_reverse_props)
  return prop_matches

def interpret_class_results(class_str):
  if isinstance(class_str, (bytes, bytearray)):
    class_str = class_str.decode('utf-8')
  if class_str == "":
    return []
  else:
    return [x.strip("'") for x in re.split('\', \'|\', "|", "|", \'', class_str[1:-1])]
    
def find_classes_of_prop_matches(classes, i_cl, candidates):
  result = []
  current_class = classes[i_cl]
  for c in candidates[:100]:
    index_request_results = index_request("#value", find_instance_type_folder(c), "subject", c)
    if index_request_results != []:
      c_classes = interpret_class_results(index_request_results[0])
      if current_class in c_classes:
        result.append(c)
  return (result, current_class)
  
def find_exact_prop_and_reverse_matches(prop, reverse, entity):
  if reverse == False:
    folder = find_direct_prop_folder(entity)
  else:
    folder = find_reverse_prop_folder(entity)
  (prop_matches, ontology_reverse_props) = strict_search_prop_in_index(prop, entity, folder, "subject", "#propval")
  return prop_matches

def find_props_of_classes_matches_strictly_or_not(props, entities, props_index, words, strictly):
  result = []
  first_result = []
  i_ent = 0
  while result == [] and i_ent < len(entities):
    i_prop = 0
    entity = entities[i_ent]
    while first_result == [] and i_prop < len(props):
      prop = props[i_prop]
      if strictly == True:
        prop_matches = find_prop_matches_strictly([prop], 0, entity, props_index, words)
      else:
        prop_matches = find_prop_matches([prop], 0, entity, props_index, words)
      if prop_matches == []:
        pass
      else:
        first_result = prop_matches[2]
        current_prop = prop_matches[0]
        current_reverse = prop_matches[1]
      i_prop += 1
    if first_result != []:
      result = first_result
      while i_prop < len(props):
        entity = entities[i_ent]
        prop_matches = find_exact_prop_and_reverse_matches(current_prop, current_reverse, entity)
        if prop_matches == []:
          pass
        else:
          result += prop_matches[2]
        i_prop += 1
    else:
      pass
    i_ent += 1
  result = list(set(result))
  if result == []:
    return ()
  else:
    return (current_prop, current_reverse, entity, result)
  
def find_props_of_classes_matches(props, entities, props_index, words):
  result = find_props_of_classes_matches_strictly_or_not(props, entities, props_index, words, True)
  if result != ():
    (current_prop, current_reverse, entity, answers) = result
    return (current_prop, current_reverse, answers)
  else:
    result = find_props_of_classes_matches_strictly_or_not(props, entities, props_index, words, False)
    if result != ():
      (current_prop, current_reverse, entity, answers) = result
      return (current_prop, current_reverse, answers)
    else:
      return ()

def try_class_then_prop_or_vice_versa(prop_matches2, classes, props1, props1_index, entity, words):
  result = []
  if prop_matches2 == []:
    return ([], (), (), (), (), (), (), ())
  else:
    i_cl = 0
    while result == [] and i_cl < len(classes):
      current_prop2 = prop_matches2[0]
      current_reverse2 = prop_matches2[1]
      candidates2 = make_short_link(prop_matches2[2])
      (class_results, current_class) = find_classes_of_prop_matches(classes, i_cl, candidates2)
      if class_results == []:
        pass
      else:
        props_of_classes_matches = find_props_of_classes_matches(props1, class_results, props1_index, words)
        if props_of_classes_matches != ():
          (current_prop1, current_reverse1, result) = props_of_classes_matches
          current_prop1 = normalise_prop_for_sparql(current_prop1)
          current_prop2 = normalise_prop_for_sparql(current_prop2)
          first_part_sparql = make_sparql_triple_x(current_prop2, current_reverse2, entity)
          second_part_sparql = make_sparql_triple_x_uri(current_prop1, current_reverse1)
          class_sparql = make_class_sparql_x(current_class)
          sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + class_sparql
          return (list(set(result)), entity, current_prop1, current_reverse1, current_prop2, current_reverse2, current_class, sparql)
      i_cl += 1
    prop_matches1 = match_second_prop(prop_matches2, props1, words, props1_index, entity)
    if prop_matches1 == ():
      pass
    else:
      i_cl = 0
      while result == [] and i_cl < len(classes):
        current_prop2 = prop_matches1[2]
        current_reverse2 = prop_matches1[3]
        current_prop1 = prop_matches1[4]
        current_reverse1 = prop_matches1[5]
        candidates2 = make_short_link(prop_matches1[0])
        (class_results, current_class) = find_classes_of_prop_matches(classes, i_cl, candidates2)
        if class_results == []:
          pass
        else:
          result = class_results
          current_prop2 = normalise_prop_for_sparql(current_prop2)
          current_prop1 = normalise_prop_for_sparql(current_prop1)
          first_part_sparql = make_sparql_triple_x(current_prop2, current_reverse2, entity)
          second_part_sparql = make_sparql_triple_x_uri(current_prop1, current_reverse1)
          class_sparql = make_class_sparql_uri(current_class)
          sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + class_sparql
          return (list(set(result)), entity, current_prop1, current_reverse1, current_prop2, current_reverse2, current_class, sparql)
        i_cl += 1
  return ([], (), (), (), (), (), (), ())

# Who is the performer of the album whose subsequent work is Willie Nelson and Family
# Which awards did the narrator of Oscar and Lucinda win
def whatPropClPropEnt(props1, classes, props2, ent, words, props1_index, props2_index, ent_index, entities):
  answer = whatPropClPropEnt_process(props1, classes, props2, ent, words, props1_index, props2_index, ent_index, entities)
  if answer in [(), []]:
    return whatPropClPropEnt_process(props2, classes, props1, ent, words, props2_index, props1_index, ent_index, entities)
  else:
    return answer
    
def whatPropClPropEnt_process(props1, classes, props2, ent, words, props1_index, props2_index, ent_index, entities):
  result = []
  i_ent = 0
  entity_uris = make_entity_uris(ent, ent_index, entities)
  while result == [] and i_ent < len(entity_uris):
    i_prop2 = 0
    entity = entity_uris[i_ent]
    while result == [] and i_prop2 < len(props2):
      if (props2_index != 0 and words[props2_index - 1].lower() in ["one", "whose", "has", "have", "had", "having", "with"]) or (props2_index >= 1 and words[props2_index - 2].lower() in ["one", "whose", "has", "have", "had", "having", "with"]) or words[props2_index].lower().endswith("'s") or ((len(words) > props2_index + 1) and words[props2_index + 1].lower().endswith("'s")) or ((len(words) > props2_index + 2) and words[props2_index + 2].lower().endswith("'s")) or (ent_index != 0 and words[ent_index - 1].lower() in ["is", "are", "was", "were"]):
        prop_matches2 = find_prop_matches_reverse(props2, i_prop2, entity, props2_index, words)
        (result, current_entity, current_prop1, current_reverse1, current_prop2, current_reverse2, current_class, sparql) = try_class_then_prop_or_vice_versa(prop_matches2, classes, props1, props1_index, entity, words)
        if result != []:
          return (result, current_entity, current_prop1, current_reverse1, current_prop2, current_reverse2, current_class, sparql)
        else:
          prop_matches2 = find_prop_matches_direct(props2, i_prop2, entity, props2_index, words)
          (result, current_entity, current_prop1, current_reverse1, current_prop2, current_reverse2, current_class, sparql) = \
            try_class_then_prop_or_vice_versa(prop_matches2, classes, props1, props1_index, entity, words)
          if result != []:
            return (result, current_entity, current_prop1, current_reverse1, current_prop2, current_reverse2, current_class, sparql)
      else:
        prop_matches2 = find_prop_matches_direct(props2, i_prop2, entity, props2_index, words)
        (result, current_entity, current_prop1, current_reverse1, current_prop2, current_reverse2, current_class, sparql) = try_class_then_prop_or_vice_versa(prop_matches2, classes, props1, props1_index, entity, words)
        if result != []:
          return (result, current_entity, current_prop1, current_reverse1, current_prop2, current_reverse2, current_class, sparql)
        else:
          prop_matches2 = find_prop_matches_reverse(props2, i_prop2, entity, props2_index, words)
          (result, current_entity, current_prop1, current_reverse1, current_prop2, current_reverse2, current_class, sparql) = \
            try_class_then_prop_or_vice_versa(prop_matches2, classes, props1, props1_index, entity, words)
          if result != []:
            return (result, current_entity, current_prop1, current_reverse1, current_prop2, current_reverse2, current_class, sparql)
      i_prop2 += 1
    i_ent += 1
  return ()

# What is the company to which Fusajiro Yamauchi proprietor to
def whatClEntProp(classes, props, ent, props_index, ent_index, words, return_all_answers, entities):
  result = []
  i_ent = 0
  entity_uris = make_entity_uris(ent, ent_index, entities)
  if return_all_answers == False:
    while result == [] and i_ent < len(entity_uris):
      i_prop = 0
      entity = entity_uris[i_ent]
      while result == [] and i_prop < len(props):
        if (props_index != 0 and words[props_index - 1].lower() in ["one", "whose", "has", "have", "had", "having", "with"]) or (props_index >= 1 and words[props_index - 2].lower() in ["one", "whose", "has", "have", "had", "having", "with"]) or (ent_index != 0 and words[ent_index - 1].lower() in ["is", "are", "was", "were"]):
          prop_matches = find_prop_matches_reverse(props, i_prop, entity, props_index, words)
          if prop_matches == []:
            pass
          else:
            i_cl = 0
            while result == [] and i_cl < len(classes):
              (current_prop, current_reverse, candidates) = prop_matches
              (result, current_class) = find_classes_of_prop_matches(classes, i_cl, candidates)
              i_cl += 1
          prop_matches = find_prop_matches_direct(props, i_prop, entity, props_index, words)
          if prop_matches == []:
            pass
          else:
            i_cl = 0
            while result == [] and i_cl < len(classes):
              (current_prop, current_reverse, candidates) = prop_matches
              (result, current_class) = find_classes_of_prop_matches(classes, i_cl, candidates)
              i_cl += 1
        else:
          prop_matches = find_prop_matches_direct(props, i_prop, entity, props_index, words)
          if prop_matches == []:
            pass
          else:
            i_cl = 0
            while result == [] and i_cl < len(classes):
              (current_prop, current_reverse, candidates) = prop_matches
              (result, current_class) = find_classes_of_prop_matches(classes, i_cl, candidates)
              i_cl += 1
          prop_matches = find_prop_matches_reverse(props, i_prop, entity, props_index, words)
          if prop_matches == []:
            pass
          else:
            i_cl = 0
            while result == [] and i_cl < len(classes):
              (current_prop, current_reverse, candidates) = prop_matches
              (result, current_class) = find_classes_of_prop_matches(classes, i_cl, candidates)
              i_cl += 1
        i_prop += 1
      i_ent += 1
    if result == []:
      return ()
    else:
      current_prop = normalise_prop_for_sparql(current_prop)
      uri_prop_sparql = make_sparql_triple_uri(current_prop, current_reverse, entity)
      class_sparql = make_class_sparql_uri(current_class)
      sparql = "SELECT DISTINCT ?uri WHERE {" + uri_prop_sparql + class_sparql
      return (remove_duplicates_preserve_order(result), entity, current_prop, current_reverse, current_class, sparql)
  else:
    all_results = []
    while i_ent < len(entity_uris):
      i_prop = 0
      entity = entity_uris[i_ent]
      while i_prop < len(props):
        prop_matches = find_all_prop_matches(props, i_prop, entity, props_index, words)
        if prop_matches == []:
          pass
        else:
          i_cl = 0
          while i_cl < len(classes):
            prop_match_i = 0
            while prop_match_i < len(prop_matches):
              (current_prop, current_reverse, candidates) = prop_matches[prop_match_i]
              (result, current_class) = find_classes_of_prop_matches(classes, i_cl, candidates)
              if result != []:
                all_results.append((result, entity, current_prop, current_reverse, current_class)) 
              prop_match_i += 1
            i_cl += 1
        i_prop += 1
      i_ent += 1
    return all_results
  
def whatPropEnt(props, ent, props_index, ent_index, words, return_all_answers, entities):
  i_ent = 0
  entity_uris = make_entity_uris(ent, ent_index, entities)
  if return_all_answers == False:
    result = find_props_of_classes_matches_strictly_or_not(props, entity_uris, props_index, words, True)
    if result != ():
      prop = normalise_prop_for_sparql(result[0])
      reverse = result[1]
      entity = result[2]
      answers = result[3]
      first_part_sparql = make_sparql_triple_uri(prop, reverse, entity)
      sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + "}"
      return (answers, entity, prop, reverse, sparql)
    else:
      result = find_props_of_classes_matches_strictly_or_not(props, entity_uris, props_index, words, False)
      if result != ():
        prop = normalise_prop_for_sparql(result[0])
        reverse = result[1]
        entity = result[2]
        answers = result[3]
        first_part_sparql = make_sparql_triple_uri(prop, reverse, entity)
        sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + "}"
        return (answers, entity, prop, reverse, sparql)
      return result
  else:
    all_results = []
    while i_ent < len(entity_uris):
      i_prop = 0
      entity = entity_uris[i_ent]
      (direct_props, reverse_props) = find_all_props_of_ent(entity)
      while i_prop < len(props):
        full_prop = get_full_prop(props[i_prop])
        prop_matches1 = all_non_strict_props(full_prop, entity, False, direct_props)
        prop_matches2 = all_non_strict_props(full_prop, entity, True, reverse_props)
        prop_matches = prop_matches1 + prop_matches2
        if prop_matches == []:
          pass
        else:
          for (p, rev, res) in prop_matches:
            all_results.append((res, entity, p, rev)) # (result, entity, current_prop, current_reverse)
        i_prop += 1
      i_ent += 1
    return all_results

def get_found_props(props_search_result):
  if props_search_result == []:
    found_props = []
  else:
    found_props_minus_brackets = [x.decode("utf-8")[1:-1] for x in props_search_result if len(x) > 2]
    found_props = interpret_prop_results(", ".join(found_props_minus_brackets))
  return found_props
  
def find_all_props_of_ent(entity):
  props_search1 = index_request("#propval", find_direct_prop_folder(entity), "subject", entity)
  props_search2 = index_request("#propval", find_reverse_prop_folder(entity), "subject", entity)
  return (get_found_props(props_search1), get_found_props(props_search2))

def get_full_prop(prop):
  if prop.endswith("_O"):
    return "ontology/" + prop[:-2]
  else:
    return "property/" + prop[:-2]
    
def match_second_prop(prop_matches1, props2, words, props2_index, ent):
  if prop_matches1 == []:
    return ()
  else:
    current_prop1 = prop_matches1[0]
    current_reverse1 = prop_matches1[1]
    result1 = prop_matches1[2]
    i_prop2 = 0
    while i_prop2 < len(props2):
      i_res1 = 0
      result = []
      while i_res1 < len(result1):
        prop_matches2 = find_prop_matches_strictly(props2, i_prop2, result1[i_res1], props2_index, words)
        if prop_matches2 == []:
          pass
        else:
          current_prop2 = prop_matches2[0]
          current_reverse2 = prop_matches2[1]
          result = prop_matches2[2]
          i_res1 += 1
          while i_res1 < len(result1):
            prop_matches2 = find_prop_matches_strictly(props2, i_prop2, result1[i_res1], props2_index, words)
            if prop_matches2 == []:
              i_res1 += 1
            else:
              if prop_matches2[0] == current_prop2 and prop_matches2[1] == current_reverse2:
                result += prop_matches2[2]
                i_res1 += 1
              else:
                i_res1 += 1
          return (remove_duplicates_preserve_order(result), ent, current_prop1, current_reverse1, current_prop2, current_reverse2)
        i_res1 += 1
      i_prop2 += 1
    i_prop2 = 0
    while i_prop2 < len(props2):
      i_res1 = 0
      result = []
      while i_res1 < len(result1):
        prop_matches2 = find_prop_matches(props2, i_prop2, result1[i_res1], props2_index, words)
        if prop_matches2 == []:
          pass
        else:
          current_prop2 = prop_matches2[0]
          current_reverse2 = prop_matches2[1]
          result = prop_matches2[2]
          i_res1 += 1
          while i_res1 < len(result1):
            prop_matches2 = find_prop_matches(props2, i_prop2, result1[i_res1], props2_index, words)
            if prop_matches2 == []:
              i_res1 += 1
            else:
              if prop_matches2[0] == current_prop2 and prop_matches2[1] == current_reverse2:
                result += prop_matches2[2]
                i_res1 += 1
              else:
                i_res1 += 1
          return (remove_duplicates_preserve_order(result), ent, current_prop1, current_reverse1, current_prop2, current_reverse2)
        i_res1 += 1
      i_prop2 += 1
    return ()
    
def whatPropPropEnt(props1, props2, ent, words, props1_index, props2_index, ent_index, entities):
  if (props2_index > 0 and words[props2_index - 1].lower() == "as") or (props2_index > 1 and words[props2_index - 2].lower() == "as"):
    props1_copy = props1.copy()
    props1_index_copy = props1_index
    props2_copy = props2.copy()
    props2_index_copy = props2_index
    props2 = props1_copy
    props2_index = props1_index_copy
    props1_index = props2_index_copy
    props1 = props2_copy
  i_ent = 0
  entity_uris = make_entity_uris(ent, ent_index, entities)
  while i_ent < len(entity_uris):
    i_prop1 = 0
    entity = entity_uris[i_ent]
    while i_prop1 < len(props1):
      prop_matches1 = find_prop_matches_direct(props1, i_prop1, entity, props1_index, words)
      answer = match_second_prop(prop_matches1, props2, words, props2_index, entity)
      if answer == ():
        prop_matches1 = find_prop_matches_reverse(props1, i_prop1, entity, props1_index, words)
        answer = match_second_prop(prop_matches1, props2, words, props2_index, entity)
        if answer == ():
          pass
        else:
          current_prop2 = normalise_prop_for_sparql(answer[2])
          current_reverse2 = answer[3]
          current_prop1 = normalise_prop_for_sparql(answer[4])
          current_reverse1 = answer[5]
          entity = answer[1]
          first_part_sparql = make_sparql_triple_x(current_prop2, current_reverse2, entity)
          second_part_sparql = make_sparql_triple_x_uri(current_prop1, current_reverse1)
          sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + "}"
          return (answer[0], entity, current_prop2, current_reverse2, current_prop1, current_reverse1, sparql)
      else:
        current_prop2 = normalise_prop_for_sparql(answer[2])
        current_reverse2 = answer[3]
        current_prop1 = normalise_prop_for_sparql(answer[4])
        current_reverse1 = answer[5]
        entity = answer[1]
        first_part_sparql = make_sparql_triple_x(current_prop2, current_reverse2, entity)
        second_part_sparql = make_sparql_triple_x_uri(current_prop1, current_reverse1)
        sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + "}"
        return (answer[0], entity, current_prop2, current_reverse2, current_prop1, current_reverse1, sparql)
      i_prop1 += 1
    i_ent += 1
  return ()

############################

def whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, ent2_index, entities, properties, classes, words):
  first_part_results = categorise_simple_parse(parse[:3], entities, properties, classes, words, False)
  if len(first_part_results) == 6: # if it includes class
    (results1, ent1, prop1, reverse1, class1, sparql) = first_part_results
    class_element = [x for x in parse[:3] if x in classes][0]
    second_part_with_class = [class_element] + parse[3:]
    second_part_results = categorise_simple_parse(second_part_with_class, entities, properties, classes, words, False)
    if second_part_results == ():
      return () # NEW (results1, ent1, prop1, reverse1, class1)
    else:
      if len(second_part_results) != 6:
        return ()
      else:
        (results2, ent2, prop2, reverse2, class2, sparql) = second_part_results
        result_intersection = list(set(results1) & set(results2))
        if result_intersection != []:
          first_part_sparql = make_sparql_triple_uri(prop1, reverse1, ent1)
          second_part_sparql = make_sparql_triple_uri(prop2, reverse2, ent2)
          class_sparql = make_class_sparql_uri(class1)
          sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + class_sparql
          return (result_intersection, ent1, prop1, reverse1, ent2, prop2, reverse2, class1, sparql)
        else:
          return ()
  elif len(first_part_results) == 5: # if it does not include class
    (results1, ent1, prop1, reverse1, sparql) = first_part_results
    second_part_results = categorise_simple_parse(parse[3:], entities, properties, classes, words, False)
    if second_part_results == ():
      return () # NEW (results1, ent1, prop1, reverse1)
    else:
      return find_intersection_without_class(second_part_results, results1, ent1, prop1, reverse1, parse[:3], parse[3:], \
                                             entities, properties, classes, words)
  elif len(first_part_results) == 7: # if it took another property by mistake
    new_parse = [x for x in parse if x not in classes]
    return whatPropEntPropEnt(new_parse, props1, entity1, props2, entity2, entities, properties, classes, words)
  elif first_part_results == ():
    return () #whatPropClPropEnt(props1, cl, props2, entity2, words, props1_index, props2_index, ent2_index, entities)

def whatPropEntPropEnt(parse, props1, entity1, props2, entity2, entities, properties, classes, words):
  first_part_results = categorise_simple_parse(parse[:2], entities, properties, classes, words, False)
  second_part_results = categorise_simple_parse(parse[2:], entities, properties, classes, words, False)
  if second_part_results == () or first_part_results == ():
    return () # (results1, ent1, prop1, reverse1, class1)
  else:
    (results1, ent1, prop1, reverse1, sparql1) = first_part_results
    return find_intersection_without_class(second_part_results, results1, ent1, prop1, reverse1, parse[:2], parse[2:], \
                                           entities, properties, classes, words)

############################

verb_properties = ["placed", "based", "founded", "found", "founds", "founding", "broadcast", "broadcasts", "broadcasted", "broadcasting", "associate", "associates", "associated", "associating", "authore", "authores", "authored", 'authoring', 'produce', 'produces', 'produced', 'producing', 'present', 'presents', 'presented', 'presenting', 'build', 'builds', 'built', 'building', 'influence', 'influences', 'influenced', 'influencing', 'maintain', 'maintains', 'maintained', 'maintaining', 'voice', 'voices', 'voiced', 'voicing', 'record', 'records', 'recorded', 'recording', 'star', 'stars', 'starred', 'starring', 'paint', 'paints', 'painted', 'painting', 'perform', 'performs', 'performed', 'performing', 'serve', 'serves', 'served', 'serving', 'edit', 'edits', 'edited', 'editing', 'develop', 'develops', 'developed', 'developing', 'fight', 'fights', 'fought', 'fighting', 'study', 'studies', 'studied', 'studying', 'illustrate', 'illustrates', 'illustrated', 'illustrating', 'discover', 'discovers', 'discovered', 'discovering', 'coach', 'coaches', 'coached', 'coaching', 'run', 'runs', 'ran', 'running', 'employ', 'employs', 'employed', 'employing', 'inspire', 'inspires', 'inspired', 'inspiring', 'narrate', 'narrates', 'narrated', 'narrating', 'command', 'commands', 'commanded', 'commanding', 'beatify', 'beatifies', 'beatified', 'beatifying', 'write', 'writes', 'wrote', 'written', 'writing', 'distribute', 'distributes', 'distributed', 'distributing', 'participate', 'participates', 'participated', 'participating', 'sing', 'sings', 'sang', 'sung', 'singing', 'cost', 'costs', 'costing', 'appoint', 'appoints', 'appointed', 'appointing', 'manage', 'manages', 'managed', 'managing', 'win', 'wins', 'won', 'winning', 'host', 'hosts', 'hosted', 'hosting', 'precede', 'precedes', 'preceded', 'preceding', 'make', 'makes', 'made', 'making', 'manufacture', 'manufactures', 'manufactured', 'manufacturing', 'cross', 'crosses', 'crossed', 'crossing', 'own', 'owns', 'owned', 'owning', 'publish', 'publishes', 'published', 'publishing', 'get', 'gets', 'got', 'getting', 'receive', 'receives', 'received', 'receiving', 'canonize', 'canonizes', 'canonized', 'canonizing', 'canonise', 'canonises', 'canonised', 'canonising', 'pen', 'pens', 'penned', 'penning', 'head', 'heads', 'headed', 'heading', 'start', 'starts', 'started', 'starting', 'commence', 'commences', 'commenced', 'commencing', 'telecast', 'telecasts', 'telecasted', 'telecasting', 'end', 'ends', 'ended', 'ending', 'create', 'creates', 'created', 'creating', 'release', 'releases', 'released', 'releasing', 'operate', 'operates', 'operated', 'operating', 'have', 'has', 'had', 'having', 'affiliate', 'affiliates', 'affiliated', 'affiliating', 'succeed', 'succeeds', 'succeeded', 'succeeding', 'compose', 'composes', 'composed', 'composing', 'play', 'plays', 'played', 'playing', 'train', 'trains', 'trained', 'training', 'design', 'designs', 'designed', 'designing', 'direct', 'directs', 'directed', 'directing', 'rule', 'rules', 'ruled', 'ruling', 'exist', 'exists', 'existed', 'existing', 'cover', 'pole', 'owner', 'owners', 'manage', 'manage', 'manage', 'manages', 'manages', 'manages', 'managed', 'managed', 'managed', 'managing', 'managing', 'managing', 'development', 'flow', 'flows', 'flowed', 'flowing', 'power', 'come', 'comes', 'came', 'coming', 'award', 'awards', 'awarded', 'awarded', 'awarded', 'famous', 'famous', 'famous', 'judge', 'judges', 'judged', 'judging', 'known', 'compose', 'composes', 'composed', 'composing', 'breed', 'breeds', 'bred', 'breeding', 'hold', 'holds', 'held', 'holding', 'lead', 'leads', 'led', 'leading', 'do', 'does', 'did', 'doing', 'act', 'acts', 'acted', 'acting', 'collaborate', 'collaborates', 'collaborated', 'collaborating', 'connect', 'connects', 'connected', 'connecting', 'bury', 'buries', 'buried', 'burying', 'die', 'dies', 'died', 'dead', 'dying', 'live', 'lives', 'lived', 'living', 'study', 'studies', 'studied', 'studying', 'educate', 'educates', 'educated', 'educating', 'locate', 'locates', 'located', 'locating', 'born', 'go', 'goes', 'went', 'gone', 'going', 'belong', 'belongs', 'belonged', 'belonging', 'associate', 'associates', 'associated', 'associating', 'originate', 'originates', 'originated', 'originating', 'sign', 'signs', 'signed', 'signing', 'mouth', 'mouth', 'relate', 'relates', 'related', 'relating', 'system', 'phd', 'take', 'takes', 'took', 'taken', 'taking', 'fly', 'flies', 'flied', 'flying', 'headquartered', 'work', 'work', 'works', 'worked', 'working', 'compete', 'competes', 'competed', 'competing', 'demise', 'cast', 'casts', 'casted', 'casting', 'follow', 'follows', 'followed', 'following', 'use', 'used', 'using', 'debut', 'debuts', 'debuted', 'debuting', 'sculpt', 'sculpts', 'sculpted', 'sculpting', 'govern', 'governs', 'governed', 'governing']

def check_verb_properties(parses, properties):
  n_ps = []
  for parse in parses:
    props_in_parse = [x for x in parse if x in properties]
    if len(props_in_parse) > 2:
      for p in props_in_parse:
        if p[1][0][0] in verb_properties:
          parse_copy = parse[:]
          parse_copy.remove(p)
          n_ps.append(parse_copy)
    elif len(props_in_parse) > 1:
      n_ps.append(parse)
      parse_copy = parse[:]
      for p in props_in_parse:
        parse_copy = parse[:]
        if p[1][0][0] in verb_properties:
          parse_copy.remove(p)
          n_ps.append(parse_copy)
  return n_ps
  
def check_two_classes(parses, classes):
  if parses == []:
    return []
  else:
    new_parses = []
    for parse in parses:
      classes_in_parse = []
      for x in parse:
        if x in classes:
          classes_in_parse.append(x)
      if len(classes_in_parse) > 1:
        pass
      else:
        new_parses.append(parse)
    return new_parses

def try_one_entity(parses, entities):
  if parses == []:
    return []
  else:
    new_parses = []
    for parse in parses:
      entities_in_parse = [x for x in parse if x in entities]
      if len(entities_in_parse) > 1:
        for e in entities_in_parse:
          new_parse = parse[:]
          new_parse.remove(e)
          new_parses.append(new_parse)
    return new_parses

def prop_for_class_replacement(parses, properties, classes, words):
  new_parses = []
  for parse in parses:
    classes_in_parse = [x for x in parse if x in classes]
    if len(classes_in_parse) == 0:
      properties_in_parse = []
      ind = 0
      for x in parse:
        if x in properties:
          properties_in_parse.append((ind, x))
        ind += 1
      if properties_in_parse == []:
        new_parses.append(parse)
      else:
        alternatives_for_parse = []
        for p in properties_in_parse:
          coinciding_classes = [x for x in classes if x[0] == p[1][0]]
          if coinciding_classes == []:
            new_parses.append(parse)
          else:
            coinciding_class = coinciding_classes[0]
            try:
              if coinciding_class[0] + len(coinciding_class[1][0]) < len(words) and \
                 words[coinciding_class[0] + len(coinciding_class[1][0])].lower() in ["one", "whose", "that", "which", "who"]:
                score = 1
              elif coinciding_class[0] + len(coinciding_class[1][0]) + 1 < len(words) and \
                   words[coinciding_class[0] + len(coinciding_class[1][0]) + 1].lower() in ["one", "whose", "that", "which", "who"]:
                score = 1
              else:
                score = 0
            except:
              score = 0
            alternatives_for_parse.append((parse[:p[0]] + [coinciding_class] + parse[p[0] + 1:], score))
        if alternatives_for_parse != []:
          alternatives_for_parse.sort(key = lambda x: x[1], reverse = True)
          alternatives_for_parse = [x[0] for x in alternatives_for_parse]
          new_parses += alternatives_for_parse
            
    else:
      new_parses.append(parse)
  return new_parses

def check_PropOfEntIsPropOfEnt(parse, entities, properties, classes, words):
  result = False
  category_parse = get_category_parse(parse, entities, properties, classes)
  if category_parse == ['PROPERTY', 'ENTITY', 'PROPERTY', 'ENTITY']:
    prop1 = parse[0]
    ent1 = parse[1]
    prop1_indixes_taken = range(prop1[0], prop1[0] + len(prop1[1][0]))
    w_i = 0
    words_between_first_propEnt = []
    while w_i < len(words):
      if w_i > prop1_indixes_taken[-1] and w_i < ent1[0]:
        words_between_first_propEnt.append(words[w_i])
      w_i += 1
    if "of" in [w.lower() for w in words_between_first_propEnt]:
      prop2 = parse[2]
      ent2 = parse[3]
      prop2_indixes_taken = range(prop2[0], prop2[0] + len(prop2[1][0]))
      w_i = 0
      words_between_second_propEnt = []
      while w_i < len(words):
        if w_i > prop2_indixes_taken[-1] and w_i < ent2[0]:
          words_between_second_propEnt.append(words[w_i])
        w_i += 1
      if "of" in [w.lower() for w in words_between_second_propEnt]:
        result = True
  return result

def check_prop_following_verb(properties_in_parse, score, words):
  for p in properties_in_parse:
    if p[1][0][0] in verb_properties:
      following_possible_prop = [] # e.g. How many islands belong to archipelagos located in the pacific - "archipelago" is more preferable than "belong to"
      other_properties_in_parse = [x for x in properties_in_parse if x != p]
      for x in other_properties_in_parse:
        p_indixes_taken = range(p[0], p[0] + len(p[1][0]))
        if x[0] > p_indixes_taken[-1]:
          w_i = 0
          words_between_props = []
          while w_i < len(words):
            if w_i > p_indixes_taken[-1] and w_i < x[0]:
              words_between_props.append(words[w_i])
            w_i += 1
          if words_between_props == []: 
            score -= 2
          elif [w.lower() for w in words_between_props] in [["to"], ["to", "a"], ["to", "the"], ["in"], ["in", "a"], ["in", "the"], ["for"], ["for", "a"], ["for", "the"]]:
            score -= 2
  return score

def rank_alternative_parses(parses, entities, properties, classes, words):
  if parses == []:
    return []
  else:
    ranked_parses = []
    for parse in parses:
      properties_in_parse = [x for x in parse if x in properties]
      if len(properties_in_parse) > 2:
        pass
      else:
        entities_in_parse = [x for x in parse if x in entities]
        if entities_in_parse == []:
          pass
        else:
          entities_in_parse.sort(key = lambda x: x[0])
          classes_in_parse = [x for x in parse if x in classes]
          matching_words = flat_list([e[1] for e in entities_in_parse]) + flat_list([p[1][0] for p in properties_in_parse]) + flat_list([c[1][0] for c in classes_in_parse])
          matching_stop_words = []
          matching_words_without_stop_words = []
          for x in matching_words:
            if x.lower() in stop_words:
              matching_stop_words.append(x)
            else:
              matching_words_without_stop_words.append(x)
          score = len(matching_words_without_stop_words) + (len(matching_stop_words) / 2.0)
          words_lower = [w.lower() for w in words]
          if len(entities_in_parse) > 1:
            if check_PropOfEntIsPropOfEnt(parse, entities, properties, classes, words) == True:
              pass
            elif list(set(words_lower) & set(["which", "that", "whose", "who"])) == []:
              score -= 4
          score = check_prop_following_verb(properties_in_parse, score, words)
          ranked_parses.append((parse, score))
    ranked_parses.sort(key = lambda x: x[1], reverse = True)
    return [x[0] for x in ranked_parses]

def add_double_replacements(combinations_of_replacements, parse, parses):
  for (r1, r2) in combinations_of_replacements:
    coinciding_elements = [x for x in parse if (x != r1[1] and x[0] == r1[1][0]) or (x != r2[1] and x[0] == r2[1][0])]
    if coinciding_elements == []:
      new_parse = parse[:]
      new_parse.remove(r1[1])
      new_parse.remove(r2[1])
      new_parse += [r1[2], r2[2]]
      new_parse.sort(key = lambda x: x[0])
      parses.append(new_parse)
  return parses

def remove_one_prop(parses, properties):
  new_parses = []
  for parse in parses:
    properties_in_parse = [x for x in parse if x in properties]
    if len(properties_in_parse) < 2:
      pass
    else:
      for prop in properties_in_parse:
        new_parse = parse[:]
        new_parse.remove(prop)
        new_parses.append(new_parse)
  return new_parses

def remove_class(parses, classes):
  new_parses = []
  for parse in parses:
    classes_in_parse = [x for x in parse if x in classes]
    if classes_in_parse == []:
      pass
    else:
      for cl in classes_in_parse:
        new_parse = parse[:]
        new_parse.remove(cl)
        new_parses.append(new_parse)
  return new_parses

def check_coinciding_elements(parses):
  new_parses = []
  for parse in parses:
    pairs = [(parse[p1], parse[p2]) for p1 in range(len(parse)) for p2 in range(p1 + 1,len(parse))]
    coincide = False
    for (a, b) in pairs:
      if a[0] == b[0]:
        coincide = True
    if coincide == False:
      new_parses.append(parse)
  return new_parses
  
def get_alternative_parses(parse, entities, properties, classes, words): # Which currency is primarily used by the company which is the distributing label of VDE-Gallo Records
  parse_ents = []
  ent_index = 0
  for x in parse:
    if isinstance(x[1], list):
      parse_ents.append((ent_index, x))
    ent_index += 1
  entities_replacements = []
  for e in parse_ents: 
    e_indexes_taken = range(e[1][0], e[1][0] + len(e[1][1]))
    e_for_cl_replacement = []
    e_for_prop_replacement = []
    for c in classes:
      if c[0] in e_indexes_taken:
        e_for_cl_replacement.append((e[0], e[1], c))
    for p in properties:
      if p[0] in e_indexes_taken:
        e_for_prop_replacement.append((e[0], e[1], p))
    entities_replacements += e_for_cl_replacement + e_for_prop_replacement
  classes_in_parse = []
  class_index = 0
  for x in parse:
    if x in classes:
      classes_in_parse.append((class_index, x))
    class_index += 1
  class_for_prop_replacements = []
  for c in classes_in_parse:
    for p in properties:
      if p[0] == c[1][0]:
        class_for_prop_replacements.append((c[0], c[1], p))
  
  properties_in_parse = []
  prop_index = 0
  for x in parse:
    if x in properties:
      properties_in_parse.append((prop_index, x))
    prop_index += 1
  
  prop_for_class_replacements = []
  for p in properties_in_parse:
    for c in classes:
      if c[0] == p[1][0]:
        prop_for_class_replacements.append((p[0], p[1], c))
  
  prop_for_prop_replacements = []
  for p1 in properties_in_parse:
    indexes_taken_by_entities = flat_list([range(x[0], x[0] + len(x[1])) for x in parse if x in entities])
    indexes_taken_by_other_props_and_classes = flat_list([range(x[0], x[0] + len(x[1][0])) for x in parse if x != p1[1] and (p in properties or p in classes)])
    indexes_taken = indexes_taken_by_entities + indexes_taken_by_other_props_and_classes
    for p2 in properties:
      p2_indexes_taken = range(p2[0], p2[0] + len(p2[1][0]))
      if p2[0] == p1[1][0] or list(set(p2_indexes_taken) & set(indexes_taken)) == []:
        prop_for_prop_replacements.append((p1[0], p1[1], p2))
  ent_class_combinations_of_replacements = list(itertools.product(*[entities_replacements, class_for_prop_replacements]))
  ent_prop_combinations_of_replacements = list(itertools.product(*[entities_replacements, prop_for_prop_replacements]))
  prop_class_combinations_of_replacements = list(itertools.product(*[prop_for_prop_replacements, class_for_prop_replacements]))
  triple_replacements = list(itertools.product(*[entities_replacements, prop_for_prop_replacements, class_for_prop_replacements]))
  new_parses = []
  for cr in class_for_prop_replacements:
    coinciding_elements = [x for x in parse if x != cr[1] and x[0] == cr[1][0]]
    if coinciding_elements == []:
      new_parses.append(parse[:cr[0]] + [cr[2]] + parse[cr[0] + 1:])
  for pr in prop_for_prop_replacements:
    coinciding_elements = [x for x in parse if x != pr[1] and x[0] == pr[1][0]]
    if coinciding_elements == []:
      new_parses.append(parse[:pr[0]] + [pr[2]] + parse[pr[0] + 1:])
  for er in entities_replacements:
    coinciding_elements = [x for x in parse if x != er[1] and x[0] == er[1][0]]
    if coinciding_elements == []:
      new_parses.append(parse[:er[0]] + [er[2]] + parse[er[0] + 1:])
  for pr in prop_for_class_replacements:
    coinciding_elements = [x for x in parse if x != pr[1] and x[0] == pr[1][0]]
    if coinciding_elements == []:
      new_parses.append(parse[:pr[0]] + [pr[2]] + parse[pr[0] + 1:])
  new_parses = add_double_replacements(ent_class_combinations_of_replacements, parse, new_parses)
  new_parses = add_double_replacements(ent_prop_combinations_of_replacements, parse, new_parses)
  new_parses = add_double_replacements(prop_class_combinations_of_replacements, parse, new_parses)
  for (r1, r2, r3) in triple_replacements:
    coinciding_elements = [x for x in parse if (x != r1[1] and x[0] == r1[1][0]) or (x != r2[1] and x[0] == r2[1][0]) or (x != r3[1] and x[0] == r3[1][0])]
    if coinciding_elements == []:
      new_parse = parse[:]
      new_parse.remove(r1[1])
      new_parse.remove(r2[1])
      new_parse.remove(r3[1])
      new_parse += [r1[2], r2[2], r3[2]]
      new_parse.sort(key = lambda x: x[0])
      new_parses.append(new_parse)
  new_parses = check_two_classes(new_parses, classes)
  new_parses = new_parses + check_verb_properties(new_parses, properties) + check_verb_properties([parse], properties)
  new_parses = prop_for_class_replacement(new_parses, properties, classes, words)
  new_parses += (try_one_entity([parse], entities) + try_one_entity(new_parses, entities))
  new_parses += remove_one_prop(new_parses, properties)
  new_parses += remove_class(new_parses, classes)
  if parse in new_parses:
    new_parses.remove(parse)
  new_new_parses = []
  for x in new_parses:
    if x not in new_new_parses and x != parse:
      new_new_parses.append(x)
  new_new_parses = check_coinciding_elements(new_new_parses)
  new_new_parses = rank_alternative_parses(new_new_parses, entities, properties, classes, words)
  return new_new_parses
  
############################

def get_category_parse(parse, entities, properties, classes):
  category_parse = []
  for x in parse:
    if x in entities:
      category_parse.append("ENTITY")
    elif x in classes:
      category_parse.append("CLASS")
    else:
      category_parse.append("PROPERTY")
  return category_parse
  
def categorise_parse_without_alternatives(parse, entities, properties, classes, words, return_all_answers):
  parse.sort(key = lambda x: x[0])
  category_parse = get_category_parse(parse, entities, properties, classes)
  if category_parse == ['CLASS', 'PROPERTY', 'ENTITY']:
    entity = "_".join(parse[2][1])
    ent_index = parse[2][0]
    props = parse[1][1][1]
    props_index = parse[1][0]
    cl = parse[0][1][1]
    return whatClEntProp(cl, props, entity, props_index, ent_index, words, return_all_answers, entities)
  elif category_parse == ['CLASS', 'ENTITY', 'PROPERTY']:
    entity = "_".join(parse[1][1])
    ent_index = parse[1][0]
    props = parse[2][1][1]
    props_index = parse[2][0]
    cl = parse[0][1][1]
    return whatClEntProp(cl, props, entity, props_index, ent_index, words, return_all_answers, entities)
  elif category_parse == ['PROPERTY', 'ENTITY', 'CLASS']:
    entity = "_".join(parse[1][1])
    ent_index = parse[1][0]
    props = parse[0][1][1]
    props_index = parse[0][0]
    cl = parse[2][1][1]
    return whatClEntProp(cl, props, entity, props_index, ent_index, words, return_all_answers, entities)
  elif category_parse == ['ENTITY', 'PROPERTY', 'CLASS']:
    entity = "_".join(parse[0][1])
    ent_index = parse[0][0]
    props = parse[1][1][1]
    props_index = parse[1][0]
    cl = parse[2][1][1]
    return whatClEntProp(cl, props, entity, props_index, ent_index, words, return_all_answers, entities)
  elif category_parse == ['PROPERTY', 'ENTITY']:
    entity = "_".join(parse[1][1])
    ent_index = parse[1][0]
    props = parse[0][1][1]
    props_index = parse[0][0]
    return whatPropEnt(props, entity, props_index, ent_index, words, return_all_answers, entities)
  elif category_parse == ['PROPERTY', 'ENTITY', 'PROPERTY']:
    entity = "_".join(parse[1][1])
    ent_index = parse[1][0]
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    props2 = parse[2][1][1]
    props2_index= parse[2][0]
    answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      props1 = parse[0][1][1]
      props1_index = parse[0][0]
      props2 = parse[2][1][1]
      props2_index= parse[2][0]
      return whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
    else:
      return answer
  elif category_parse == ['ENTITY', 'PROPERTY']:
    entity = "_".join(parse[0][1])
    ent_index = parse[0][0]
    props = parse[1][1][1]
    props_index = parse[1][0]
    return whatPropEnt(props, entity, props_index, ent_index, words, return_all_answers, entities)
  elif category_parse == ['PROPERTY', 'PROPERTY', 'ENTITY']:
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    props2 = parse[0][1][1]
    props2_index= parse[0][0]
    entity = "_".join(parse[2][1])
    ent_index = parse[2][0]
    answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      props1 = parse[0][1][1]
      props1_index = parse[0][0]
      props2 = parse[1][1][1]
      props2_index= parse[1][0]
      return whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
    else:
      return answer
  elif category_parse == ['ENTITY', 'PROPERTY', 'PROPERTY']:
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    props2 = parse[2][1][1]
    props2_index= parse[2][0]
    entity = "_".join(parse[0][1])
    ent_index = parse[0][0]
    answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      props1 = parse[2][1][1]
      props1_index = parse[2][0]
      props2 = parse[1][1][1]
      props2_index= parse[1][0]
      return whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
    else:
      return answer
  elif category_parse == ['PROPERTY', 'CLASS', 'PROPERTY', 'ENTITY']:
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    cl = parse[1][1][1]
    props2 = parse[2][1][1]
    props2_index= parse[2][0]
    entity = "_".join(parse[3][1])
    ent_index = parse[3][0]
    return whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
  elif category_parse == ['ENTITY', 'PROPERTY', 'CLASS', 'PROPERTY']:
    props1 = parse[3][1][1]
    props1_index = parse[3][0]
    cl = parse[2][1][1]
    props2 = parse[1][1][1]
    props2_index= parse[1][0]
    entity = "_".join(parse[0][1])
    ent_index = parse[0][0]
    return whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
  elif category_parse == ['PROPERTY', 'CLASS', 'ENTITY', 'PROPERTY']:
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    cl = parse[1][1][1]
    props2 = parse[3][1][1]
    props2_index= parse[3][0]
    entity = "_".join(parse[2][1])
    ent_index = parse[2][0]
    return whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
  elif category_parse == ['PROPERTY', 'ENTITY', 'PROPERTY', 'CLASS']:
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    cl = parse[3][1][1]
    props2 = parse[2][1][1]
    props2_index= parse[2][0]
    entity = "_".join(parse[1][1])
    ent_index = parse[1][0]
    return whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
  elif category_parse == ['CLASS', 'PROPERTY', 'ENTITY', 'PROPERTY']:
    props1 = parse[3][1][1]
    props1_index = parse[3][0]
    cl = parse[0][1][1]
    props2 = parse[1][1][1]
    props2_index= parse[1][0]
    entity = "_".join(parse[2][1])
    ent_index = parse[2][0]
    return whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
  elif category_parse == ['CLASS', 'PROPERTY', 'ENTITY', 'ENTITY']:
    prop = [parse[1]]
    cl = [parse[0]]
    entity1 = [parse[2]]
    entity2 = [parse[3]]
    return sole_entity_after_and_type(entity2, entity1, prop, cl, entities, properties, classes, words)
  elif category_parse == ['CLASS', 'ENTITY', 'ENTITY', 'PROPERTY']:
    prop = [parse[3]]
    cl = [parse[0]]
    entity1 = [parse[1]]
    entity2 = [parse[2]]
    return sole_entity_after_and_type(entity2, entity1, prop, cl, entities, properties, classes, words)
  elif category_parse == ['CLASS', 'PROPERTY', 'ENTITY', 'PROPERTY', 'ENTITY']:
    cl = parse[0][1][1]
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    entity1 = "_".join(parse[2][1])
    props2 = parse[3][1][1]
    props2_index = parse[3][0]
    entity2 = "_".join(parse[4][1])
    entity2_index = parse[4][0]
    return whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
  elif category_parse == ['PROPERTY', 'CLASS', 'ENTITY', 'PROPERTY', 'ENTITY']:
    cl = parse[1][1][1]
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    entity1 = "_".join(parse[2][1])
    props2 = parse[3][1][1]
    props2_index = parse[3][0]
    entity2 = "_".join(parse[4][1])
    entity2_index = parse[4][0]
    return whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
  elif category_parse == ['PROPERTY', 'ENTITY', 'CLASS', 'PROPERTY', 'ENTITY']:
    cl = parse[2][1][1]
    props1 = parse[0][1][1]
    props1_index = parse[1][0]
    entity1 = "_".join(parse[1][1])
    props2 = parse[3][1][1]
    props2_index = parse[3][0]
    entity2 = "_".join(parse[4][1])
    entity2_index = parse[4][0]
    return whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
  elif category_parse == ['PROPERTY', 'ENTITY', 'CLASS', 'ENTITY', 'PROPERTY']:
    cl = parse[2][1][1]
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    entity1 = "_".join(parse[1][1])
    props2 = parse[4][1][1]
    props2_index = parse[4][0]
    entity2 = "_".join(parse[3][1])
    entity2_index = parse[3][0]
    return whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
  elif category_parse == ['ENTITY', 'PROPERTY', 'CLASS', 'PROPERTY', 'ENTITY']:
    cl = parse[2][1][1]
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    entity1 = "_".join(parse[0][1])
    props2 = parse[3][1][1]
    props2_index = parse[3][0]
    entity2 = "_".join(parse[4][1])
    entity2_index = parse[4][0]
    return whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
  elif category_parse == ['ENTITY', 'PROPERTY', 'CLASS', 'ENTITY', 'PROPERTY']:
    cl = parse[2][1][1]
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    entity1 = "_".join(parse[0][1])
    props2 = parse[4][1][1]
    props2_index = parse[4][0]
    entity2 = "_".join(parse[3][1])
    entity2_index = parse[3][0]
    return whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
  elif category_parse == ['PROPERTY', 'ENTITY', 'PROPERTY', 'ENTITY']:
    props1 = parse[0][1][1]
    entity1 = "_".join(parse[1][1])
    props2 = parse[2][1][1]
    entity2 = "_".join(parse[3][1])
    return whatPropEntPropEnt(parse, props1, entity1, props2, entity2, entities, properties, classes, words)
  elif category_parse == ['PROPERTY', 'ENTITY', 'ENTITY', 'PROPERTY']:
    props1 = parse[0][1][1]
    entity1 = "_".join(parse[1][1])
    props2 = parse[3][1][1]
    entity2 = "_".join(parse[2][1])
    return whatPropEntPropEnt(parse, props1, entity1, props2, entity2, entities, properties, classes, words)
  elif category_parse == ['CLASS', 'PROPERTY', 'PROPERTY', 'ENTITY']:
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    cl = parse[0][1][1]
    props2 = parse[2][1][1]
    props2_index= parse[2][0]
    entity = "_".join(parse[3][1])
    ent_index = parse[3][0]
    return whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
  else:
    return ()

def try_alternative_parses(parse, entities, properties, classes, words):
  alternative_parses = get_alternative_parses(parse, entities, properties, classes, words)
  alternative_parses = check_neighbouring_properties(alternative_parses, properties, words)
  for p in alternative_parses:
    answer = categorise_parse_without_alternatives(p, entities, properties, classes, words, False)
    if answer != ():
      return answer
  return ()
  
def categorise_simple_parse(parse, entities, properties, classes, words, return_all_answers):
  parse.sort(key = lambda x: x[0])
  category_parse = []
  for x in parse:
    if x in entities:
      category_parse.append("ENTITY")
    elif x in classes:
      category_parse.append("CLASS")
    else:
      category_parse.append("PROPERTY")
  if category_parse == ['CLASS', 'PROPERTY', 'ENTITY']:
    entity = "_".join(parse[2][1])
    ent_index = parse[2][0]
    props = parse[1][1][1]
    props_index = parse[1][0]
    cl = parse[0][1][1]
    answer = whatClEntProp(cl, props, entity, props_index, ent_index, words, return_all_answers, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['CLASS', 'ENTITY', 'PROPERTY']:
    entity = "_".join(parse[1][1])
    ent_index = parse[1][0]
    props = parse[2][1][1]
    props_index = parse[2][0]
    cl = parse[0][1][1]
    answer = whatClEntProp(cl, props, entity, props_index, ent_index, words, return_all_answers, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['PROPERTY', 'ENTITY', 'CLASS']:
    entity = "_".join(parse[1][1])
    ent_index = parse[1][0]
    props = parse[0][1][1]
    props_index = parse[0][0]
    cl = parse[2][1][1]
    answer = whatClEntProp(cl, props, entity, props_index, ent_index, words, return_all_answers, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['ENTITY', 'PROPERTY', 'CLASS']:
    entity = "_".join(parse[0][1])
    ent_index = parse[0][0]
    props = parse[1][1][1]
    props_index = parse[1][0]
    cl = parse[2][1][1]
    answer = whatClEntProp(cl, props, entity, props_index, ent_index, words, return_all_answers, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['PROPERTY', 'ENTITY']:
    entity = "_".join(parse[1][1])
    ent_index = parse[1][0]
    props = parse[0][1][1]
    props_index = parse[0][0]
    answer = whatPropEnt(props, entity, props_index, ent_index, words, return_all_answers, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['ENTITY', 'PROPERTY']:
    entity = "_".join(parse[0][1])
    ent_index = parse[0][0]
    props = parse[1][1][1]
    props_index = parse[1][0]
    answer = whatPropEnt(props, entity, props_index, ent_index, words, return_all_answers, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['PROPERTY', 'PROPERTY', 'ENTITY']:
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    props2 = parse[0][1][1]
    props2_index= parse[0][0]
    entity = "_".join(parse[2][1])
    ent_index = parse[2][0]
    answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      props1 = parse[0][1][1]
      props1_index = parse[0][0]
      props2 = parse[1][1][1]
      props2_index= parse[1][0]
      answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
      if answer == ():
        answer = try_alternative_parses(parse, entities, properties, classes, words)
      return answer
    else:
      return answer
  elif category_parse == ['PROPERTY', 'ENTITY', 'PROPERTY']:
    entity = "_".join(parse[1][1])
    ent_index = parse[1][0]
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    props2 = parse[2][1][1]
    props2_index= parse[2][0]
    answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      props1 = parse[0][1][1]
      props1_index = parse[0][0]
      props2 = parse[2][1][1]
      props2_index= parse[2][0]
      answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
      if answer == ():
        answer = try_alternative_parses(parse, entities, properties, classes, words)
      return answer
    else:
      return answer
  elif category_parse == ['ENTITY', 'PROPERTY', 'PROPERTY']:
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    props2 = parse[2][1][1]
    props2_index= parse[2][0]
    entity = "_".join(parse[0][1])
    ent_index = parse[0][0]
    answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      props1 = parse[2][1][1]
      props1_index = parse[2][0]
      props2 = parse[1][1][1]
      props2_index= parse[1][0]
      answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
      if answer == ():
        answer = try_alternative_parses(parse, entities, properties, classes, words)
      return answer
    else:
      return answer
  elif category_parse == ['PROPERTY', 'CLASS', 'PROPERTY', 'ENTITY']:
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    cl = parse[1][1][1]
    props2 = parse[2][1][1]
    props2_index= parse[2][0]
    entity = "_".join(parse[3][1])
    ent_index = parse[3][0]
    answer = whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['ENTITY', 'PROPERTY', 'CLASS', 'PROPERTY']:
    props1 = parse[3][1][1]
    props1_index = parse[3][0]
    cl = parse[2][1][1]
    props2 = parse[1][1][1]
    props2_index= parse[1][0]
    entity = "_".join(parse[0][1])
    ent_index = parse[0][0]
    answer = whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['PROPERTY', 'CLASS', 'ENTITY', 'PROPERTY']:
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    cl = parse[1][1][1]
    props2 = parse[3][1][1]
    props2_index= parse[3][0]
    entity = "_".join(parse[2][1])
    ent_index = parse[2][0]
    answer = whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['PROPERTY', 'ENTITY', 'PROPERTY', 'CLASS']:
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    cl = parse[3][1][1]
    props2 = parse[2][1][1]
    props2_index= parse[2][0]
    entity = "_".join(parse[1][1])
    ent_index = parse[1][0]
    answer = whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['CLASS', 'PROPERTY', 'ENTITY', 'PROPERTY']:
    props1 = parse[3][1][1]
    props1_index = parse[3][0]
    cl = parse[0][1][1]
    props2 = parse[1][1][1]
    props2_index= parse[1][0]
    entity = "_".join(parse[2][1])
    ent_index = parse[2][0]
    answer = whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      props1 = parse[1][1][1]
      props1_index = parse[1][0]
      props2 = parse[3][1][1]
      props2_index= parse[3][0]
      answer = whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
      if answer == ():
        answer = try_alternative_parses(parse, entities, properties, classes, words)
      return answer
    else:
      return answer
  elif category_parse == ['CLASS', 'PROPERTY', 'ENTITY', 'ENTITY']:
    prop = [parse[1]]
    cl = [parse[0]]
    entity1 = [parse[2]]
    entity2 = [parse[3]]
    answer = sole_entity_after_and_type(entity2, entity1, prop, cl, entities, properties, classes, words)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['CLASS', 'ENTITY', 'ENTITY', 'PROPERTY']:
    prop = [parse[3]]
    cl = [parse[0]]
    entity1 = [parse[1]]
    entity2 = [parse[2]]
    answer = sole_entity_after_and_type(entity2, entity1, prop, cl, entities, properties, classes, words)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['CLASS', 'PROPERTY', 'ENTITY', 'PROPERTY', 'ENTITY']:
    cl = parse[0][1][1]
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    entity1 = "_".join(parse[2][1])
    props2 = parse[3][1][1]
    props2_index = parse[3][0]
    entity2 = "_".join(parse[4][1])
    entity2_index = parse[4][0]
    answer = whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['PROPERTY', 'CLASS', 'ENTITY', 'PROPERTY', 'ENTITY']:
    cl = parse[1][1][1]
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    entity1 = "_".join(parse[2][1])
    props2 = parse[3][1][1]
    props2_index = parse[3][0]
    entity2 = "_".join(parse[4][1])
    entity2_index = parse[4][0]
    answer = whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['PROPERTY', 'ENTITY', 'CLASS', 'PROPERTY', 'ENTITY']:
    cl = parse[2][1][1]
    props1 = parse[0][1][1]
    props1_index = parse[1][0]
    entity1 = "_".join(parse[1][1])
    props2 = parse[3][1][1]
    props2_index = parse[3][0]
    entity2 = "_".join(parse[4][1])
    entity2_index = parse[4][0]
    answer = whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['PROPERTY', 'ENTITY', 'CLASS', 'ENTITY', 'PROPERTY']:
    cl = parse[2][1][1]
    props1 = parse[0][1][1]
    props1_index = parse[0][0]
    entity1 = "_".join(parse[1][1])
    props2 = parse[4][1][1]
    props2_index = parse[4][0]
    entity2 = "_".join(parse[3][1])
    entity2_index = parse[3][0]
    answer = whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['ENTITY', 'PROPERTY', 'CLASS', 'PROPERTY', 'ENTITY']:
    cl = parse[2][1][1]
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    entity1 = "_".join(parse[0][1])
    props2 = parse[3][1][1]
    props2_index = parse[3][0]
    entity2 = "_".join(parse[4][1])
    entity2_index = parse[4][0]
    answer = whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['ENTITY', 'PROPERTY', 'CLASS', 'ENTITY', 'PROPERTY']:
    cl = parse[2][1][1]
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    entity1 = "_".join(parse[0][1])
    props2 = parse[4][1][1]
    props2_index = parse[4][0]
    entity2 = "_".join(parse[3][1])
    entity2_index = parse[3][0]
    answer = whatClPropEntPropEnt(parse, cl, props1, entity1, props2, entity2, props1_index, props2_index, entity2_index, entities, properties, classes, words)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['PROPERTY', 'ENTITY', 'PROPERTY', 'ENTITY']:
    props1 = parse[0][1][1]
    entity1 = "_".join(parse[1][1])
    props2 = parse[2][1][1]
    entity2 = "_".join(parse[3][1])
    answer = whatPropEntPropEnt(parse, props1, entity1, props2, entity2, entities, properties, classes, words)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['PROPERTY', 'ENTITY', 'ENTITY', 'PROPERTY']:
    props1 = parse[0][1][1]
    entity1 = "_".join(parse[1][1])
    props2 = parse[3][1][1]
    entity2 = "_".join(parse[2][1])
    answer = whatPropEntPropEnt(parse, props1, entity1, props2, entity2, entities, properties, classes, words)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
  elif category_parse == ['CLASS', 'PROPERTY', 'PROPERTY', 'ENTITY']:
    props1 = parse[1][1][1]
    props1_index = parse[1][0]
    cl = parse[0][1][1]
    props2 = parse[2][1][1]
    props2_index= parse[2][0]
    entity = "_".join(parse[3][1])
    ent_index = parse[3][0]
    answer = whatPropClPropEnt(props1, cl, props2, entity, words, props1_index, props2_index, ent_index, entities)
    if answer == ():
      answer = try_alternative_parses(parse, entities, properties, classes, words)
    return answer
    """
  elif category_parse == ['ENTITY', 'PROPERTY', 'PROPERTY', 'ENTITY']:
    coinciding_prop = [x for x in properties if parse[0][0] == x[0]] # if entity 1 coincides with some property
    if coinciding_prop == []:
      answer = try_alternative_parses(parse, entities, properties, classes, words)
      return answer
    else:
      props2 = coinciding_prop[0][1][1]
      props2_index = coinciding_prop[0][0]
      props1 = parse[2][1][1]
      props1_index= parse[2][0]
      entity = "_".join(parse[3][1])
      ent_index = parse[3][0]
      answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
      if answer == ():
        props1 = parse[1][1][1]
        props1_index= parse[1][0]
        answer = whatPropPropEnt(props1, props2, entity, words, props1_index, props2_index, ent_index, entities)
      return answer
    """
  else:
    alternative_parses = get_alternative_parses(parse, entities, properties, classes, words)
    alternative_parses = check_neighbouring_properties(alternative_parses, properties, words)
    for p in alternative_parses:
      answer = categorise_parse_without_alternatives(p, entities, properties, classes, words, False)
      if answer != () and answer != None:
        return answer
      else:
        pass
    return ()
    
def check_neighbouring_class_and_entity(parses, entities, classes):
  new_parses = []
  classes = []
  for p in parses:
    for element in p:
      if element in entities:
        entity = element
      elif element in classes:
        classes.append(element)
    if classes == [] or (classes[0][0] != entity[0] - 1 and classes[0][0] != entity[0] + len(entity[1])):
      new_parses.append(p)
  return new_parses

def check_neighbouring_properties(parses, properties, words_without_question_words):
  new_parses_share = [] # to exclude "share" as property 
  for parse in parses:
    properties_in_parse = [x for x in parse if x in properties]
    if len(properties_in_parse) in [0, 1]:
      new_parses_share.append(parse)
    else:
      share_prop = [x for x in properties_in_parse if x[1][0] == ['share']]
      if share_prop == []:
        new_parses_share.append(parse)
      else:
        share_prop = share_prop[0]
        next_prop = [x for x in properties_in_parse if x[0] == share_prop[0] + 1]
        if next_prop == []:
          new_parses_share.append(parse)
        else:
          new_parses_share.append([x for x in parse if x != share_prop])
  new_parses_belong = []
  if (len(properties) == 2 and [x for x in properties if x[1][0] == ['belong']] != []) or (len(properties) == 3 and [x for x in properties if x[1][0] in [['belong'], ['belong', 'to']]] != []):
    belong_prop = [x for x in properties if x[1][0] in [['belong'], ['belong', 'to']]]
    properties = [x for x in properties if x not in belong_prop]
    for parse in new_parses_share:
      belong_prop_in_parse = [x for x in parse if x in belong_prop]
      if belong_prop_in_parse == []:
        new_parses_belong.append(parse)
  else:
    new_parses_belong = new_parses_share
  new_parses = []
  for parse in new_parses_belong:
    properties_in_parse = [x for x in parse if x in properties]
    if len(properties_in_parse) in [0, 1]:
      new_parses.append(parse)
    else:
      pairs = [(properties_in_parse[p1], properties_in_parse[p2]) for p1 in range(len(properties_in_parse)) for p2 in range(p1+1,len(properties_in_parse))]
      neighbouring = False
      for (p1, p2) in pairs:
        if p1[1][0][0] in verb_properties or p2[1][0][0] in verb_properties: # How many people are there whose children died in Indiana
          neighbouring = False
        elif (p1[0] >= p2[0] and p1[0] <= p2[0] + len(p2[1][0])) or (p2[0] >= p1[0] and p2[0] <= p1[0] + len(p1[1][0])):
          neighbouring = True
          #if (p1[0] + len(p1[1][0]) == p2[0] or p2[0] + len(p2[1][0]) == p1[0]) and p1[1][0][0] not in verb_properties and p2[1][0][0] not in verb_properties:
          #neighbouring = True
          # but if we have "'s" between them, it's ok (e.g Which show's theme music composer's label is MapleMusic Recordings?)
          last_word_of_first_prop_in_words = words_without_question_words[p1[0] + len(p1[1][0]) - 1].lower()
          if last_word_of_first_prop_in_words.endswith("'s") and p1[0] + len(p1[1][0]) == p2[0]:
            neighbouring = False
          last_word_of_second_prop_in_words = words_without_question_words[p2[0] + len(p2[1][0]) - 1].lower()
          if last_word_of_first_prop_in_words.endswith("'s") and p2[0] + len(p2[1][0]) == p1[0]:
            neighbouring = False
      if neighbouring == False:
        new_parses.append(parse)
      else:
        pass
  return new_parses

def check_neighbouring_properties_ranked(parses, properties, words):
  new_parses = []
  for (parse, rank) in parses:
    properties_in_parse = [x for x in parse if x in properties]
    if len(properties_in_parse) in [0, 1]:
      new_parses.append((parse, rank))
    else:
      pairs = [(properties_in_parse[p1], properties_in_parse[p2]) for p1 in range(len(properties_in_parse)) for p2 in range(p1+1,len(properties_in_parse))]
      neighbouring = False
      for (p1, p2) in pairs:
        if p1[1][0][0] in verb_properties or p2[1][0][0] in verb_properties: # How many people are there whose children died in Indiana
          neighbouring = False
        elif (p1[0] >= p2[0] and p1[0] <= p2[0] + len(p2[1][0])) or (p2[0] >= p1[0] and p2[0] <= p1[0] + len(p1[1][0])):
          neighbouring = True
          #if (p1[0] + len(p1[1][0]) == p2[0] or p2[0] + len(p2[1][0]) == p1[0]) and p1[1][0][0] not in verb_properties and p2[1][0][0] not in verb_properties:
          #neighbouring = True
          # but if we have "'s" between them, it's ok (e.g Which show's theme music composer's label is MapleMusic Recordings?)
          last_word_of_first_prop_in_words = words[p1[0] + len(p1[1][0]) - 1].lower()
          if last_word_of_first_prop_in_words.endswith("'s") and p1[0] + len(p1[1][0]) == p2[0]:
            neighbouring = False
          last_word_of_second_prop_in_words = words[p2[0] + len(p2[1][0]) - 1].lower()
          if last_word_of_first_prop_in_words.endswith("'s") and p2[0] + len(p2[1][0]) == p1[0]:
            neighbouring = False
      if neighbouring == False:
        new_parses.append((parse, rank))
      else:
        pass
  return new_parses
  
def intersecting_and_nonintersecting(all_combinations):
  intersecting = []
  nonintersecting = []
  for x in all_combinations:
    if find_intersecting_elements(x) == True:
      intersecting.append(x)
    else:
      nonintersecting.append(x)
  return (intersecting, nonintersecting)

def find_best_entity_yes_no(entities, words):
  ents_with_ranks = []
  for e in entities:
    e_str = str(" ".join(e[1]))
    e_lst = e_str.split()
    right_words = words[e[0]:]
    right_words_str = str(" ".join(right_words))
    right_words_lst = right_words_str.split()[:len(e_lst)]
    pairs = zip(e_lst, right_words_lst)
    matches = rank_pairs(pairs, 0)
    if "(" in e_str and "(" not in right_words_str:
      matches -= 0.25
    ents_with_ranks.append((e, matches))
  ents_with_ranks.sort(key = lambda x: x[1], reverse = True)
  return ents_with_ranks[0][0]

def yes_no_search(first_entity_uris, second_entity_uris):
  new_first_entity_uris = []
  for x in first_entity_uris:
    if isinstance(x, (bytes, bytearray)):
      new_first_entity_uris.append(x.decode('utf-8'))
    else:
      new_first_entity_uris.append(x)
  new_second_entity_uris = []
  for x in second_entity_uris:
    if isinstance(x, (bytes, bytearray)):
      new_second_entity_uris.append(x.decode('utf-8'))
    else:
      new_second_entity_uris.append(x)
  first_entity_uris = new_first_entity_uris
  second_entity_uris = new_second_entity_uris
  i_ent1 = 0
  while i_ent1 < len(first_entity_uris):
    entity1 = first_entity_uris[i_ent1]
    props_search = index_request("#propval", find_direct_prop_folder(entity1), "subject", entity1)
    found_props_minus_brackets = [x.decode("utf-8")[1:-1] for x in props_search if len(x) > 2]
    found_props = interpret_prop_results(", ".join(found_props_minus_brackets))
    matching_prop_val = []
    if found_props != [['']]:
      for [p, v] in found_props:
        if v in second_entity_uris:
          matching_prop_val.append((entity1, p, v))
      if matching_prop_val != []:
        result = matching_prop_val
        return result
      i_ent1 += 1
    else:
      i_ent1 += 1
  return ()
  
def yes_no_question(entities, properties, words_without_question_words, all_words):
  entities.sort(key = lambda x: x[0])
  first_ent_index = entities[0][0]
  first_ent_candidates = [x for x in entities if x[0] == first_ent_index or x[0] == first_ent_index + 1]
  first_entity = find_best_entity_yes_no(first_ent_candidates, words_without_question_words)
  last_words_index = len(words_without_question_words) - 1
  first_entity_uris = make_entity_uris("_".join(first_entity[1]), first_entity[0], entities)
  second_ent_candidates = [x for x in entities if x[0] + len(x[1]) - 1 == last_words_index]
  for second_candidate in second_ent_candidates:
    #second_entity = find_best_entity_yes_no(second_ent_candidates, words_without_question_words)
    second_entity_uris = make_entity_uris("_".join(second_candidate[1]), second_candidate[0], entities)
    result = yes_no_search(first_entity_uris, second_entity_uris)
    if result == () or result == []:
      result = yes_no_search(second_entity_uris, first_entity_uris)
      if result != () and result != []:
        return result
      else:
        pass
    else:
      return result
  return ()

def delimiter_of_complex_sentence(words):
  words_lower = [x.lower() for x in words]
  phrase = " ".join(words_lower)
  which_is_also_lst = ["which is also", "that is also", "which are also", "that are also", "which was also", "that was also", "which were also", "that were also"]
  is_also_lst = ["is also", "are also", "was also", "were also"]
  if any(s in phrase for s in which_is_also_lst):
    which_and_that_indexes = [i for i,val in enumerate(words) if val == "which" or val == "that"]
    for i in which_and_that_indexes:
      if len(words) > i + 2 and words[i + 1] in ["is", "are", "was", "were"] and words[i + 2] == "also":
        return (i, i + 2)
    return ()
  elif any(s in phrase for s in is_also_lst) or "which once" in phrase:
    is_and_are_indexes = [i for i,val in enumerate(words) if val in ["is", "are", "was", "were", "which"]]
    for i in is_and_are_indexes:
      if len(words) > i + 1 and words[i + 1] in ["also", "once"] and i > 2:
        return (i, i + 1)
    return ()
  elif "also" in phrase:
    also_indexes = [i for i,val in enumerate(words) if val == "also"]
    return (also_indexes[0], also_indexes[0])
  else:
    return ()
    
def and_as_part_of_entity(entities, words):
  if ("and" in [x.lower() for x in words]) or ("nad" in [x.lower() for x in words]):
    and_indexes = [i for i,val in enumerate(words) if val in ["and", "nad"]]
    independent_and = []
    for ind in and_indexes:
      entities_with_and = [(i, e) for (i, e) in entities if ind - i > 0 and len(e) > ind - i and e[ind - i].lower() in ["and", "nad"]]
      if entities_with_and == []:
        independent_and.append(ind)
    return independent_and
  else:
    return []

# new

def intersection(lst1, lst2): 
  lst3 = list((mset(lst1) & mset(lst2)).elements()) #[value for value in lst1 if value in lst2] 
  lst2_genitive = [x + "'s" for x in lst2]
  lst4 = [x[:-2] for x in list((mset(lst1) & mset(lst2_genitive)).elements())] #[value[:-2] for value in lst1 if value in lst2_genitive] 
  lst1_without_punctuation = [x[:-1] for x in lst1 if x[-1].isalpha() == False]
  lst5 = list((mset(lst1_without_punctuation) & mset(lst2)).elements()) #[value for value in lst1_without_punctuation if value in lst2] 
  lst2_plural = [x + "s" for x in lst2]
  lst6 = list((mset(lst1) & mset(lst2_plural)).elements())
  return lst3 + lst4 + lst5 + lst6

def remove_non_ascii(word):
  for w in word:
    if all(ord(char) < 128 for char in w):
      pass
    else:
      word = word.replace(w, "")
  return word
 
def check_participation_uppercase_words(combinations, words_without_question_words): # What company is the one which wrote the google web toolkit and PlayN -- don't consider PlayN, consider only the first part
  lower_words_without_question_words = [remove_non_ascii(x.lower()) for x in words_without_question_words]
  words_without_question_words_non_ascii_removed = [remove_non_ascii(x) for x in words_without_question_words]
  if lower_words_without_question_words == words_without_question_words or words_without_question_words == [remove_non_ascii(x) for x in words_without_question_words]:
    return True
  else:
    all_lower_words_of_combinations = []
    for combination in combinations:
      all_lower_words_of_combination = get_lower_words_from_parse(combination[1])
      all_lower_words_of_combinations += all_lower_words_of_combination
    all_lower_words_of_combinations_sorted = list(set(all_lower_words_of_combinations))
    for word in all_lower_words_of_combinations_sorted:
      if word in lower_words_without_question_words and word not in words_without_question_words_non_ascii_removed:
        return False
    return True

def get_lower_words_from_parse(combination):
  all_lower_words = []
  for component in combination:
    if isinstance(component[1], tuple):
      lower_words = [remove_non_ascii(x.lower()) for x in component[1][0]]
    else:
      lower_words = [remove_non_ascii(x.lower()) for x in component[1]]
    all_lower_words += lower_words
  return all_lower_words
  
# new
def arrange_by_coverage(combinations, words_without_question_words):
  lower_words_without_question_words = [remove_non_ascii(x.lower()) for x in words_without_question_words]
  new_combinations = []
  for combination in combinations:
    n = 0
    all_lower_words = get_lower_words_from_parse(combination)
    intersecting = intersection(lower_words_without_question_words, all_lower_words)
    n += len(intersecting)
    for w in all_lower_words:
      if w not in intersecting:
        n -= 1
    new_combinations.append((n, combination))
  new_combinations.sort(key = lambda x: x[0], reverse = True)
  if check_participation_uppercase_words(new_combinations, words_without_question_words):
    return [x[1] for x in new_combinations]
  else:
    new_new_combinations = [] # What system is both a platform where Nord runs and also distributed The beauty inside ("Nord" is preferred more than entity "A platform")
    for (n, combination) in new_combinations:
      all_words = []
      for component in combination:
        if isinstance(component[1], tuple):
          words = [remove_non_ascii(x) for x in component[1][0]]
        else:
          words = [remove_non_ascii(x) for x in component[1]]
        all_words += words
      for w in all_words:
        if w.lower() != w and w in words_without_question_words:
          n += 1
        elif w.lower() != w and w not in words_without_question_words:
          n -= 1
      new_new_combinations.append((n, combination))
    new_new_combinations.sort(key = lambda x: x[0], reverse = True)
    return [x[1] for x in new_new_combinations]
  
def best_prop_ent_class_combination(entities, properties, classes, words_without_question_words, one_entity):
  combinations_with_classes = list(itertools.product(*[entities, properties, classes]))
  combinations_without_classes = list(itertools.product(*[entities, properties]))
  all_combinations = [list(x) for x in combinations_with_classes + combinations_without_classes]
  (intersecting, nonintersecting) = intersecting_and_nonintersecting(all_combinations)
  nonintersecting_second_prop = [find_second_prop(x, words_without_question_words, properties) for x in nonintersecting]
  if one_entity == True:
    nonintersecting_arranged = arrange_by_matches(nonintersecting_second_prop, entities, properties, classes, words_without_question_words)
    neighbouring_class_and_entity = check_neighbouring_class_and_entity(nonintersecting_arranged, entities, classes)
    neighbouring_properties = check_neighbouring_properties(neighbouring_class_and_entity, properties, words_without_question_words)
    return arrange_by_coverage(neighbouring_properties, words_without_question_words)
  else:
    nonintersecting_second_prop_and_ent = [find_second_ent(x, words_without_question_words, entities) for x in nonintersecting_second_prop]
    nonintersecting_arranged = arrange_by_matches(nonintersecting_second_prop_and_ent, entities, properties, classes, words_without_question_words)
    neighbouring_class_and_entity = check_neighbouring_class_and_entity(nonintersecting_arranged, entities, classes)
    neighbouring_properties = check_neighbouring_properties(neighbouring_class_and_entity, properties, words_without_question_words)
    return arrange_by_coverage(neighbouring_properties, words_without_question_words)
    
def best_prop_ent_combination(entities, properties, classes, words_without_question_words):
  all_combinations = list(itertools.product(*[entities, properties]))
  all_combinations = [list(x) for x in all_combinations]
  (intersecting, nonintersecting) = intersecting_and_nonintersecting(all_combinations)
  return arrange_by_matches(nonintersecting, entities, properties, classes, words_without_question_words)

############################

def try_all_combinations_of_props(parse, entities, properties, classes, words_without_question_words):
  entity_element = [e for e in parse if e in entities][0]
  entity = "_".join(entity_element[1])
  props_combinations = list(itertools.product(*[properties, properties]))
  props_combinations = [(x,y) for (x,y) in props_combinations if x != y]
  result = []
  prop_pair_i = 0
  while result == [] and prop_pair_i < len(props_combinations):
    prop_pair = list(props_combinations[prop_pair_i])
    prop_pair.sort(key = lambda z: z[0])
    props1 = prop_pair[1][1][1]
    props2 = prop_pair[0][1][1]
    props1_index = prop_pair[1][0]
    props2_index = prop_pair[0][0]
    i_prop1 = 0
    prop_matches1 = []
    while i_prop1 < len(props1):
      prop_matches1 += find_all_prop_matches(props1, i_prop1, entity, props1_index, words_without_question_words)
      i_prop1 += 1
    if prop_matches1 == []:
      pass
    else:
      for (prop1, prop_reverse1, results1) in prop_matches1:
        prop_matches2 = []
        i_prop2 = 0
        while i_prop2 < len(props2):
          for r in results1:
            prop_matches2 += find_all_prop_matches(props2, i_prop2, r, props2_index, words_without_question_words)
          if prop_matches2 != []:
            for (prop2, prop_reverse2, results2) in prop_matches2:
              result += results2
            return (remove_duplicates_preserve_order(result), prop1, prop_reverse1, prop2, prop_reverse2, entity)
          i_prop2 += 1
    prop_pair_i += 1
  return ()

############################

#find_best_entity_yes_no(entities, words)

def try_all_combinations_of_ents_and_props(entities, properties, words_without_question_words, all_words):
  arranged_entities = arrange_exact_entity_matches(entities, words_without_question_words)
  for e in arranged_entities:
    entity_str = "_".join(e[1])
    ent_index = e[0]
    entity_uris = make_entity_uris(entity_str, ent_index, entities)
    for uri in entity_uris:
      answer = best_prop_for_selected_ent(uri, e, properties, words_without_question_words)
      if answer == ():
        pass
      else:
        return answer
  for e in arranged_entities:
    entity_str = "_".join(e[1])
    ent_index = e[0]
    entity_uris = make_entity_uris(entity_str, ent_index, entities)
    for uri in entity_uris:
      answer = try_origin_props(uri, words_without_question_words, all_words)
      if answer == ():
        pass
      else:
        return answer
  return ()

def capitalise_first(w):
  if len(w) == 1:
    return w.upper()
  else:
    return w[0].upper() + w[1:]

def find_partly_matching_props(direct_props, reverse_props, entity_link, remaining_words_minus_stop_words, non_intersecting_props_words):
  reverse_i = 0
  for found_props in [direct_props, reverse_props]:
    if reverse_i == 0:
      reverse = False
    else:
      reverse = True
    if found_props != []:
      results = []
      probable_props = []
      for [prop, val] in found_props:
        prop = shorten_prop(prop)
        prop_words = re.findall('[A-Z][^A-Z]*', capitalise_first(prop))
        prop_words = [x.lower() for x in prop_words]
        matching_words = []
        for w in list(set(remaining_words_minus_stop_words + non_intersecting_props_words)):
          w = w.lower()
          if w in prop_words or w + "s" in prop_words or w + "es" in prop_words or w[:-1] + "ies" in prop_words \
             or w[:-1] in prop_words or (len(w) > 3 and w[:-3] + "y" in prop_words) or prop.lower().startswith(w) or prop.lower().endswith(w):
            matching_words.append(w)
        rank = len(matching_words)
        probable_props.append(((prop, val), rank))
      probable_props.sort(key = lambda x: x[1], reverse = True)
      max_rank = probable_props[0][1]
      if max_rank == 0:
        return ()
      else:
        most_probable_ontology_props = [p[0] for p in probable_props if p[1] == max_rank and "ontology/" in p[0][0]]
        if most_probable_ontology_props == []:
          most_probable_prop = "property/" + probable_props[0][0][0]
          answers = [probable_props[0][0][1]]
          if len(probable_props) > 1:
            for ((p, v), r) in probable_props[1:]:
              if p == most_probable_prop:
                answers.append(v)
          first_part_sparql = make_sparql_triple_uri(most_probable_prop, reverse, entity_link)
          sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + "}"
          return (answers, entity_link, most_probable_prop, reverse, sparql)
        else:
          most_probable_prop = most_probable_ontology_props[0][0]
          answers = [most_probable_ontology_props[0][1]]
          if len(most_probable_ontology_props) > 1:
            for ((p, v), r) in most_probable_ontology_props[1:]:
              if p == most_probable_prop:
                answers.append(v)
          first_part_sparql = make_sparql_triple_uri(most_probable_prop, reverse, entity_link)
          sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + "}"
          return (answers, entity_link, most_probable_prop, reverse, sparql)
    reverse_i += 1
  return ()
  
def try_origin_props(entity, words_without_question_words, all_words):
  # Where is Hafthor Julius Bjornsson from
  if " ".join(all_words).lower().startswith(("where can i find", "where can one find")):
    possible_props = ['location_O', 'location_P', 'locations_P', 'locationCity_O', 'locationCity_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P', 'stateOfOrigin_O', 'stateOfOrigin_P', 'birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'homeland_O', 'homeland_P', 'hometown_O','homeTown_P', 'bornPlace_P']
  else:
    possible_props = ['stateOfOrigin_O', 'stateOfOrigin_P', 'birthPlace_O', 'birthPlace_P', 'placeOfBirth_P', 'homeland_O', 'homeland_P', 'hometown_O','homeTown_P', 'bornPlace_P', 'locationCity_O', 'locationCity_P', 'location_O', 'location_P', 'locations_P', 'city_O', 'city_P', 'county_O', 'county_P', 'state_O', 'state_P', 'province_O', 'province_P', 'region_O', 'region_P', 'district_O', 'district_P', 'territory_O', 'territory_P']
  result = []
  i_prop = 0
  props_index = 0
  while result == [] and i_prop < len(possible_props):
    prop_matches = find_prop_matches(possible_props, i_prop, entity, props_index, words_without_question_words)
    if prop_matches == []:
      pass
    else:
      current_prop = prop_matches[0]
      current_reverse = prop_matches[1]
      result = prop_matches[2]
      first_part_sparql = make_sparql_triple_uri(current_prop, current_reverse, entity)
      sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + "}"
      return (result, entity, current_prop, current_reverse, sparql)
    i_prop += 1
  return ()
  
def best_prop_for_selected_ent(entity_link, original_ent, properties, words_without_question_words):
  entity_indexes_taken = range(original_ent[0], original_ent[0] + len(original_ent[1]))
  remaining_words = words_without_question_words[:entity_indexes_taken[0]] + words_without_question_words[entity_indexes_taken[-1]+1:]
  remaining_words_minus_stop_words = [w for w in remaining_words if w.lower() not in stop_words]
  combinations_with_props = [[original_ent, p] for p in properties]
  non_intersecting_props = [p for [e, p] in combinations_with_props if find_intersecting_elements([e, p]) == False]
  non_intersecting_props_functions = flat_list([p[1][1] for p in non_intersecting_props])
  non_intersecting_props_words = [w[:-2] for w in non_intersecting_props_functions if len(w) > 2]
  (direct_props, reverse_props) = find_all_props_of_ent(entity_link)
  if non_intersecting_props_functions != []:
    results = []
    i_prop = 0
    while i_prop < len(non_intersecting_props_functions):
      full_prop = get_full_prop(non_intersecting_props_functions[i_prop])
      prop_matches1 = all_non_strict_props(full_prop, entity_link, False, direct_props)
      prop_matches2 = all_non_strict_props(full_prop, entity_link, True, reverse_props)
      prop_matches = prop_matches1 + prop_matches2
      if prop_matches == []:
        pass
      else:
        current_prop = prop_matches[0][0]
        current_reverse = prop_matches[0][1]
        answers = prop_matches[0][2]
        first_part_sparql = make_sparql_triple_uri(current_prop, current_reverse, entity_link)
        sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + "}"
        return (answers, entity_link, current_prop, current_reverse, sparql) #((res, entity_link, p, rev)) # (result, entity, current_prop, current_reverse)
      i_prop += 1
    partly_matching_props = find_partly_matching_props(direct_props, reverse_props, entity_link, remaining_words_minus_stop_words, non_intersecting_props_words)
    if partly_matching_props != ():
      return partly_matching_props
    else:
      return ()
  else:
    partly_matching_props = find_partly_matching_props(direct_props, reverse_props, entity_link, remaining_words_minus_stop_words, non_intersecting_props_words)
    if partly_matching_props != ():
      return partly_matching_props
    else:
      return ()

def rank_ent_pairs(pairs, matches):
  for (a,b) in pairs:
    if a[-1].isalpha() == False and is_number(a[-1]) == False and is_number(a) == False and len(a) > 1: # this will also include "É", etc.
      a = a[:-1]
    if b[-1].isalpha() == False and is_number(b[-1]) == False and is_number(b) == False and len(b) > 1: # this will also include "É", etc.
      b = b[:-1]
    a_lower = a.lower()
    b_lower = b.lower()
    if a_lower == b_lower and a_lower in ["a", "the"]:
      matches += 0.5
    elif a_lower == b_lower:
      if check_capitalisation(a, b) == True:
        matches += 2
      else:
        matches += 1
    elif a_lower + "s" == b_lower or a_lower + "es" == b_lower or a_lower[:-1] + "ies" == b_lower or a_lower[:-1] == b_lower or \
        (len(a_lower) > 3 and a_lower[:-3] + "y" == b_lower) or b_lower + "s" == a_lower or b_lower + "es" == a_lower or \
        b_lower[:-1] + "ies" == a_lower or b_lower[:-1] == a_lower or (len(b_lower) > 3 and b_lower[:-3] + "y" == a_lower) or fuzz.ratio(a_lower, b_lower) > 90:
      matches += 0.5
    else:
      matches -= 0.5
  return matches

def arrange_exact_entity_matches(ents, words):
  new_ents = []
  for e in ents:
    has_bracket = False # entities without brackets are preferred if there are no brackets in the question ('Linda Hogan' is better than 'Linda Hogan (television personality)')
    matches = 0
    text_words = e[1]
    if "(" in " ".join(text_words):
      has_bracket = True
    e_str = (str(" ".join(text_words))) #.translate(None, string.punctuation)
    #e_lst_without_punctuation = e_str_without_punctuation.split()
    right_words = words[e[0]:]
    right_words_str = str(" ".join(right_words)) #.translate(None, string.punctuation)
    right_words_lst = right_words_str.split()[:len(text_words)]
    pairs = zip(text_words, right_words_lst)
    matches = rank_ent_pairs(pairs, matches)
    if has_bracket == True and "(" not in " ".join(words):
      matches -= 0.25
    new_ents.append((e, matches))
  new_ents.sort(key = lambda x: x[1], reverse = True)
  return [x[0] for x in new_ents]
  
############################

def sole_entity_after_and_type(sole_entity_after_and, entities_before_and, properties_before_and, classes_before_and, entities, properties, classes, words_without_question_words):
  prop_ent_class_before_and = best_prop_ent_class_combination(entities_before_and, properties_before_and, classes_before_and, words_without_question_words, True)
  parse_before_and = prop_ent_class_before_and[0]
  first_part_results = categorise_simple_parse(parse_before_and, entities, properties, classes, words_without_question_words, False)
  if len(first_part_results) == 6: # if it includes class
    (results1, ent1, prop1, reverse1, class1, sparql) = first_part_results
    property_element = [e for e in parse_before_and if e in properties][0]
    class_element = [e for e in parse_before_and if e in classes][0]
    parse_after_and_with_property_and_class = [class_element] + [property_element] + sole_entity_after_and
    second_part_results = categorise_simple_parse(parse_after_and_with_property_and_class, entities, properties, classes, words_without_question_words, False)
    if second_part_results == () or second_part_results == None:
      return () #(results1, ent1, prop1, reverse1, class1)
    else:
      if len(second_part_results) == 6:
        (results2, ent2, prop2, reverse2, class2, sparql) = second_part_results
        result_intersection = list(set(results1) & set(results2))
        if result_intersection != []:
          first_part_sparql = make_sparql_triple_uri(prop1, reverse1, ent1)
          second_part_sparql = make_sparql_triple_uri(prop2, reverse2, ent2)
          class_sparql = make_class_sparql_uri(class1)
          sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + class_sparql
          return (result_intersection, ent1, prop1, reverse1, ent2, prop2, reverse2, class1, sparql)
        else:
          all_first_part_results = categorise_simple_parse(parse_before_and, entities, properties, classes, words_without_question_words, True)
          all_second_part_results = categorise_simple_parse(parse_after_and_with_property_and_class, entities, properties, classes, words_without_question_words, True)
          result = []
          i = 0
          while i < len(all_first_part_results):
            j = 0
            while j < len(all_second_part_results):
              result_intersection = list(set(all_first_part_results[i][0]) & set(all_second_part_results[j][0])) 
              if result_intersection != []:
                ent1 = all_first_part_results[i][1] 
                prop1 = normalise_prop_for_sparql(all_first_part_results[i][2])
                reverse1 = all_first_part_results[i][3]
                ent2 = all_second_part_results[j][1]
                prop2 = normalise_prop_for_sparql(all_second_part_results[j][2])
                reverse2 = all_second_part_results[j][3]
                first_part_sparql = make_sparql_triple_uri(prop1, reverse1, ent1)
                second_part_sparql = make_sparql_triple_uri(prop2, reverse2, ent2)
                sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + "}"
                return (result_intersection, ent1, prop1, reverse1, ent2, prop2, reverse2, sparql)
              j += 1
            i += 1
          return ()
      else:
        return ()
  elif len(first_part_results) == 5: # if it does not include class
    (results1, ent1, prop1, reverse1, sparql) = first_part_results
    property_element = [e for e in parse_before_and if e in properties][0]
    parse_after_and_with_property = [property_element] + sole_entity_after_and
    second_part_results = categorise_simple_parse(parse_after_and_with_property, entities, properties, classes, words_without_question_words, False)
    if second_part_results == () or second_part_results == None:
      return () #return (results1, ent1, prop1, reverse1)
    else:
      (results2, ent2, prop2, reverse2, sparql) = second_part_results
      result_intersection = list(set(results1) & set(results2))
      if result_intersection != []:
        first_part_sparql = make_sparql_triple_uri(prop1, reverse1, ent1)
        second_part_sparql = make_sparql_triple_uri(prop2, reverse2, ent2)
        sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + "}"
        return (result_intersection, ent1, prop1, reverse1, ent2, prop2, reverse2, sparql)
      else:
        return find_intersection_without_class(second_part_results, results1, ent1, prop1, reverse1, parse_before_and, parse_after_and_with_property, entities, properties, classes, words_without_question_words)
  else:
    prop_ent_class_after_and = best_prop_ent_class_combination(sole_entity_after_and, properties_before_and, classes_before_and, words_without_question_words, True)
    if prop_ent_class_after_and in [(), []]:
      return ()
    else:
      parse_after_and = prop_ent_class_after_and[0]
      second_part_results = categorise_simple_parse(parse_after_and, entities, properties, classes, words_without_question_words, False)
      return second_part_results

def all_part_results_for_all_props(parse, entities, properties, classes, words_without_question_words):
  properties_in_parse = [x for x in parse if x in properties]
  results = []
  if len(properties_in_parse) > 1:
    parses = []
    parse_without_props = [x for x in parse if x not in properties_in_parse]
    for prop in properties_in_parse:
      parses.append(parse_without_props + [prop])
    for p in parses:
      result = categorise_simple_parse(p, entities, properties, classes, words_without_question_words, True)
      if isinstance(result, tuple):
        result = [result]
      results += result
  return results
  
def traverse_all_results_with_class(parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words):
  class_element = [e for e in parse_before_and if e in classes][0]
  all_first_part_results = all_part_results_for_all_props(parse_before_and, entities, properties, classes, words_without_question_words)
  all_second_part_results = all_part_results_for_all_props([class_element] + parse_after_and, entities, properties, classes, words_without_question_words)
  result = []
  i = 0
  while i < len(all_first_part_results):
    j = 0
    while j < len(all_second_part_results):
      result_intersection = list(set(all_first_part_results[i][0]) & set(all_second_part_results[j][0])) 
      if result_intersection != []:
        return (result_intersection, all_first_part_results[i][1], all_first_part_results[i][2], all_first_part_results[i][3], \
                all_second_part_results[j][1], all_second_part_results[j][2], all_second_part_results[j][3])
      j += 1
    i += 1
  if all_first_part_results != []:
    if len(all_first_part_results[0]) == 5:
      (results, ent, prop, reverse, cl) = all_first_part_results[0]
      sparql = "SELECT DISTINCT ?uri WHERE {" + make_sparql_triple_uri(prop, reverse, ent) + make_class_sparql_uri(cl)
      return (results, ent, prop, reverse, cl, sparql)
    else:
      return all_first_part_results[0]
  elif all_second_part_results != []:
    if len(all_second_part_results[0]) == 5:
      (results, ent, prop, reverse, cl) = all_second_part_results[0]
      sparql = "SELECT DISTINCT ?uri WHERE {" + make_sparql_triple_uri(prop, reverse, ent) + make_class_sparql_uri(cl)
      return (results, ent, prop, reverse, cl, sparql)
    else:
      return all_second_part_results[0]
  else:
    return []

# What is the television show whose subsequent work is Crusade (TV series) and developed by  J. Michael Straczynski? 
def find_intersection_with_class(second_part_results, results1, ent1, prop1, reverse1, cl, parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words):
  if second_part_results != ():
    if len(second_part_results) == 5:
      (results2, ent2, prop2, reverse2, sparql) = second_part_results
    elif len(second_part_results) == 6:
      (results2, ent2, prop2, reverse2, cl2, sparql) = second_part_results
    result_intersection = list(set(results1) & set(results2))
    if result_intersection != []:
      first_part_sparql = make_sparql_triple_uri(prop1, reverse1, ent1)
      second_part_sparql = make_sparql_triple_uri(prop2, reverse2, ent2)
      class_sparql = make_class_sparql_uri(cl)
      sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + class_sparql
      return (result_intersection, ent1, prop1, reverse1, ent2, prop2, reverse2, cl, sparql)
    else:
      return traverse_all_results_with_class(parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words)
  else:
    return traverse_all_results_with_class(parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words)
                                             
def find_intersection_without_class(second_part_results, results1, ent1, prop1, reverse1, parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words):
  if second_part_results == ():
    return () # (results1, ent1, prop1, reverse1)
  else:
    (results2, ent2, prop2, reverse2, sparql) = second_part_results
    result_intersection = list(set(results1) & set(results2))
    if result_intersection == []:
      all_first_part_results = categorise_simple_parse(parse_before_and, entities, properties, classes, words_without_question_words, True)
      all_second_part_results = categorise_simple_parse(parse_after_and, entities, properties, classes, words_without_question_words, True)
      if isinstance(all_first_part_results, tuple):
        all_first_part_results = [all_first_part_results]
      if isinstance(all_second_part_results, tuple):
        all_second_part_results = [all_second_part_results]
      result = []
      i = 0
      while i < len(all_first_part_results):
        j = 0
        while j < len(all_second_part_results):
          result_intersection = list(set(all_first_part_results[i][0]) & set(all_second_part_results[j][0])) 
          if result_intersection != []:
            ent1 = all_first_part_results[i][1] 
            prop1 = normalise_prop_for_sparql(all_first_part_results[i][2])
            reverse1 = all_first_part_results[i][3]
            ent2 = all_second_part_results[j][1]
            prop2 = normalise_prop_for_sparql(all_second_part_results[j][2])
            reverse2 = all_second_part_results[j][3]
            first_part_sparql = make_sparql_triple_uri(prop1, reverse1, ent1)
            second_part_sparql = make_sparql_triple_uri(prop2, reverse2, ent2)
            sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + "}"
            return (result_intersection, ent1, prop1, reverse1, ent2, prop2, reverse2, sparql)
          j += 1
        i += 1
      return () #(results1, ent1, prop1, reverse1)
    else:
      prop1 = normalise_prop_for_sparql(prop1)
      prop2 = normalise_prop_for_sparql(prop2)
      first_part_sparql = make_sparql_triple_uri(prop1, reverse1, ent1)
      second_part_sparql = make_sparql_triple_uri(prop2, reverse2, ent2)
      sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + "}"
      return (result_intersection, ent1, prop1, reverse1, ent2, prop2, reverse2, sparql)

def return_intersection(intersection):
  if len(intersection) == 7:
    (res, ent1, prop1, reverse1, ent2, prop2, reverse2) = intersection
    first_part_sparql = make_sparql_triple_uri(prop1, reverse1, ent1)
    second_part_sparql = make_sparql_triple_uri(prop2, reverse2, ent2)
    sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + "}"
    return (res, ent1, prop1, reverse1, ent2, prop2, reverse2, sparql)
  else:
    return intersection

def find_alternative_ents(entity): # Name the television show whose subsequent work is Crusade and Composer is Stewart Copeland? - Crusade
  first_word = entity[0][1][0].lower()
  all_entity_words = [x.lower() for x in entity[0][1]]
  index = entity[0][0]
  if len(first_word) == 1 or first_word[:2].isalpha() == False:
    folder = "other"
  else:
    folder = first_word[:2]
  candidates = find_entity_candidates("labelsindex/" + folder, first_word)
  result = []
  for c in candidates:
    c_without_brackets = re.sub(r' \([^)]*\)', '', c)
    if all_entity_words == c_without_brackets.lower().split() and "(disambiguation)" not in c and all_entity_words != c.lower().split():
      result.append(c)
  return [(index, x.split()) for x in result]

def get_words_from_sparql(sparql):
  matches1 = re.findall('<http://dbpedia.org/ontology/(.*?)>', sparql)
  matches2 = re.findall('<http://dbpedia.org/property/(.*?)>', sparql)
  matches3 = re.findall('<http://dbpedia.org/resource/(.*?)>', sparql)
  prop_words = flat_list([re.findall('[A-Z][^A-Z]*', capitalise_first(x)) for x in matches1 + matches2])
  words = flat_list([x.lower().split("_") for x in prop_words + matches3])
  return words
  
def choose_better_answer_from_two(first_part_results, second_part_results, words_without_question_words):
  if first_part_results in [(), []]:
    return second_part_results
  elif second_part_results in [(), []]:
    return first_part_results
  else:
    words1 = get_words_from_sparql(first_part_results[-1])
    words2 = get_words_from_sparql(second_part_results[-1])
    lower_words_without_question_words = [x.lower() for x in words_without_question_words]
    intersection1 = len([x for x in words1 if x in lower_words_without_question_words])
    intersection2 = len([x for x in words2 if x in lower_words_without_question_words])
    if intersection1 >= intersection2:
      return first_part_results
    else:
      return second_part_results

def analyse_second_part_of_complex_sentence(first_part_results, parse_before_and, parse_after_and, parses_after_and, entities, properties, classes, words_without_question_words):
  if len(first_part_results) == 6: # if it includes class
    (results1, ent1, prop1, reverse1, class1, sparql) = first_part_results
    class_element = [e for e in parse_before_and if e in classes][0]
    parse_after_and_with_class = [class_element] + parse_after_and
    second_part_results = categorise_simple_parse(parse_after_and_with_class, entities, properties, classes, words_without_question_words, False)
    intersection = find_intersection_with_class(second_part_results, results1, ent1, prop1, reverse1, class1, parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words)
    if intersection in [(), []]:
      if len(parses_after_and) > 1:
        parse_after_and_with_class = [class_element] + parses_after_and[1]
        second_part_results = categorise_simple_parse(parse_after_and_with_class, entities, properties, classes, words_without_question_words, False)
        intersection = find_intersection_with_class(second_part_results, results1, ent1, prop1, reverse1, class1, parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words)
        if intersection in [(), []]:
          return choose_better_answer_from_two(first_part_results, second_part_results, words_without_question_words)
        else:
          return return_intersection(intersection)
      else:
        return choose_better_answer_from_two(first_part_results, second_part_results, words_without_question_words)
    else:
      return return_intersection(intersection)
  elif len(first_part_results) == 5: # if it does not include class
    (results1, ent1, prop1, reverse1, sparql) = first_part_results
    second_part_results = categorise_simple_parse(parse_after_and, entities, properties, classes, words_without_question_words, False)
    if second_part_results == ():
      property_element = [e for e in parse_before_and if e in properties][0] # e.g. Which party does Iqbal Singh and B Shiva Rao currently belong to
      entity_element = [e for e in parse_after_and if e in entities][0]
      parse_after_and = [property_element] + [entity_element]
      second_part_results = categorise_simple_parse(parse_after_and, entities, properties, classes, words_without_question_words, False)
      intersection = find_intersection_without_class(second_part_results, results1, ent1, prop1, reverse1, parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words)
      if intersection in [(), []]:
        return choose_better_answer_from_two(first_part_results, second_part_results, words_without_question_words) 
      else:
        return return_intersection(intersection)
    else:
      intersection = find_intersection_without_class(second_part_results, results1, ent1, prop1, reverse1, parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words)
      if intersection in [(), []]:
        if len(parses_after_and) > 1:
          parse_after_and = parses_after_and[1]
          second_part_results = categorise_simple_parse(parse_after_and, entities, properties, classes, words_without_question_words, False)
          intersection = find_intersection_without_class(second_part_results, results1, ent1, prop1, reverse1, parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words)
          if intersection in [(), []]:
            result = find_intersection_without_class(second_part_results, results1, ent1, prop1, reverse1, parse_before_and, parse_after_and, entities, properties, classes, words_without_question_words)
            if result in [(), []]:
              return choose_better_answer_from_two(first_part_results, second_part_results, words_without_question_words)
            else:
              return result
          else:
            return return_intersection(intersection)
        else:
          return choose_better_answer_from_two(first_part_results, second_part_results, words_without_question_words)
      else:
        return return_intersection(intersection)
  else:
    second_part_results = categorise_simple_parse(parse_after_and, entities, properties, classes, words_without_question_words, False)
    return second_part_results
        
def check_where_delimiter(words):
  words_lower = [x.lower() for x in words]
  phrase = " ".join(words_lower)
  if ("is also" in phrase or "are also" in phrase or "was also" in phrase or "were also" in phrase) and "where" in words:
    where_indexes = [i for i,val in enumerate(words) if val == "where"]
    independent_where = []
    for i in where_indexes:
      phrase_after_where = " ".join(words_lower[i:])
      if ("is also" in phrase_after_where or "are also" in phrase_after_where or "was also" in phrase_after_where or "were also" in phrase_after_where):
        independent_where.append(i)
        return (independent_where[0], independent_where[0])
  else:
    return ()
    
# Which content license of the MSX BASIC is also the profession of the Laura K. Ipsen 
def complex_second_part_of_complex_sentence(entities_after_and, properties_after_and, entities_before_and, properties_before_and, classes_before_and, entities, properties, classes, words_without_question_words, words_before_and, words_after_and, all_words):
  parses_after_and = best_prop_ent_combination(entities_after_and, properties_after_and, classes, words_without_question_words)
  if parses_after_and == []:
    where_delimiter = check_where_delimiter(words_without_question_words)
    if where_delimiter == ():
      pass
    else:
      (delimiter_start, delimiter_end) = where_delimiter
      words_before_and = words_without_question_words[:delimiter_start]
      words_after_and = words_without_question_words[delimiter_end + 1:]
      entities_before_and = [(i, e) for (i, e) in entities if i < delimiter_start]
      entities_after_and = [(i, e) for (i, e) in entities if i > delimiter_end]
      properties_before_and = [(i, p) for (i, p) in properties if i < delimiter_start and delimiter_start not in range(i, len(p[0]) + i)]
      properties_after_and = [(i, p) for (i, p) in properties if i > delimiter_end]
      classes_before_and = [(i, c) for (i, c) in classes if i < delimiter_start and delimiter_start not in range(i, len(c[0]) + i)]
      parses_after_and = best_prop_ent_combination(entities_after_and, properties_after_and, classes, words_without_question_words)
      if parses_after_and == []:
        return try_all_combinations_of_ents_and_props(entities, properties, words_without_question_words, all_words)
  parse_after_and = parses_after_and[0]
  prop_ent_class_before_and = best_prop_ent_class_combination(entities_before_and, properties_before_and, classes_before_and, words_before_and, True)
  if prop_ent_class_before_and == []:
    return try_all_combinations_of_ents_and_props(entities, properties, words_without_question_words, all_words)
  else:
    parse_before_and = prop_ent_class_before_and[0]
    properties_before_and = [x for x in parse_before_and if x in properties][::-1]
    classes_before_and = [x for x in parse_before_and if x in classes]
    entity_before_and = [x for x in parse_before_and if x in entities]
    if len(properties_before_and) > 1:
      first_part_parses = []
      for p in properties_before_and:
        first_part_parses.append(classes_before_and + entity_before_and + [p])
    else:
      first_part_parses = [parse_before_and]
    for first_part_parse in first_part_parses:
      first_part_results = categorise_simple_parse(first_part_parse, entities, properties, classes, words_without_question_words, False)
      if first_part_results != ():
        return analyse_second_part_of_complex_sentence(first_part_results, parse_before_and, parse_after_and, parses_after_and, entities, properties, classes, words_without_question_words)
      else:
        alternative_ents = find_alternative_ents(entity_before_and)
        i = 0
        while first_part_results == () and i < len(alternative_ents):
          new_entities = [alternative_ents[i] if x == entity_before_and[0] else x for x in entities]
          new_parse_before_and = [alternative_ents[i] if x == entity_before_and[0] else x for x in parse_before_and]
          first_part_results = categorise_simple_parse(new_parse_before_and, new_entities, properties, classes, words_without_question_words, False)
          i += 1
        if first_part_results != ():
          return analyse_second_part_of_complex_sentence(first_part_results, parse_before_and, parse_after_and, parses_after_and, entities, properties, classes, words_without_question_words)
        else:
          all_first_part_results = categorise_simple_parse(parse_before_and, entities, properties, classes, words_without_question_words, True)
          all_second_part_results = categorise_simple_parse(parse_after_and, entities, properties, classes, words_without_question_words, True)
          result = []
          i = 0
          while i < len(all_first_part_results):
            j = 0
            while j < len(all_second_part_results):
              result_intersection = list(set(all_first_part_results[i][0]) & set(all_second_part_results[j][0])) 
              if result_intersection != []:
                ent1 = all_first_part_results[i][1] 
                prop1 = normalise_prop_for_sparql(all_first_part_results[i][2])
                reverse1 = all_first_part_results[i][3]
                ent2 = all_second_part_results[j][1]
                prop2 = normalise_prop_for_sparql(all_second_part_results[j][2])
                reverse2 = all_second_part_results[j][3]
                first_part_sparql = make_sparql_triple_uri(prop1, reverse1, ent1)
                second_part_sparql = make_sparql_triple_uri(prop2, reverse2, ent2)
                sparql = "SELECT DISTINCT ?uri WHERE {" + first_part_sparql + ". " + second_part_sparql + "}"
                return (result_intersection, ent1, prop1, reverse1, ent2, prop2, reverse2, sparql)
              j += 1
            i += 1
  return try_all_combinations_of_ents_and_props(entities, properties, words_without_question_words, all_words)
  
def remove_the_and_a(lst):
  return list(filter(lambda a: a not in ["the", "a"], [x.lower() for x in lst]))
  
def complex_sentences(entities, properties, classes, words_without_question_words, all_words, delimiter_start, delimiter_end):
  words_before_and = words_without_question_words[:delimiter_start]
  words_after_and = words_without_question_words[delimiter_end + 1:]
  entities_before_and = [(i, e) for (i, e) in entities if i < delimiter_start]
  entities_after_and = [(i, e) for (i, e) in entities if i > delimiter_end]
  properties_before_and = [(i, p) for (i, p) in properties if i < delimiter_start and delimiter_start not in range(i, len(p[0]) + i)]
  properties_after_and = [(i, p) for (i, p) in properties if i > delimiter_end]
  classes_before_and = [(i, c) for (i, c) in classes if i < delimiter_start and delimiter_start not in range(i, len(c[0]) + i)]
  sole_entity_after_and = [(i, e) for (i, e) in entities_after_and if ' '.join(e).lower() == ' '.join(remove_the_and_a(words_after_and))]
  if sole_entity_after_and != [] or properties_after_and == []:
    answer = sole_entity_after_and_type(sole_entity_after_and, entities_before_and, properties_before_and, classes_before_and, entities, properties, classes, words_without_question_words)
    if answer == ():
      return probably_simple_type(entities, properties, classes, words_without_question_words, all_words)
    else:
      return answer
  else:
    sole_entity_before_and = [(i, e) for (i, e) in entities_before_and if ' '.join(e).lower() == ' '.join(words_before_and).lower()]
    if sole_entity_before_and != [] or properties_before_and == []: # Giuseppe Bertello and Pietro Parolin are leaders of which place
      classes_after_and = [(i, c) for (i, c) in classes if delimiter_end < i]
      answer = sole_entity_after_and_type(sole_entity_before_and, entities_after_and, properties_after_and, classes_after_and, entities, properties, classes, words_without_question_words)
      if answer == ():
        return probably_simple_type(entities, properties, classes, words_without_question_words, all_words)
      else:
        return answer
    return complex_second_part_of_complex_sentence(entities_after_and, properties_after_and, entities_before_and, properties_before_and, classes_before_and, entities, properties, classes, words_without_question_words, words_before_and, words_after_and, all_words)

############################

def sublists(sublist, mainlist):
  if sublist[0] not in mainlist:
    return []
  else:
    indices = [i for i, x in enumerate(mainlist) if x == sublist[0]]
    for i in indices:
      if len(sublist) > len(mainlist[i:]):
        pass
      else:
        j = i
        matching = []
        for x in sublist:
          if x == mainlist[j]:
            matching.append(x)
          j += 1
        if matching == sublist:
          return sublist
        else:
          return []
    return []
    
def best_prop_in_simple_quest(entities, properties, classes, words_without_question_words, all_words):
  exact_entity_matches = [x for x in entities if sublists(x[1], words_without_question_words) == x[1]]
  best_entity = max(exact_entity_matches, key = lambda x:x[1]) #arrange_by_matches([[e] for e in entities], entities, properties, classes, words_without_question_words)[0][0]
  entity_indexes_taken = range(best_entity[0], best_entity[0] + len(best_entity[1]))
  remaining_words = words_without_question_words[:entity_indexes_taken[0]] + words_without_question_words[entity_indexes_taken[-1]+1:]
  remaining_words_minus_stop_words = [w for w in remaining_words if w.lower() not in stop_words]
  entity_uris = make_entity_uris("_".join(best_entity[1]), best_entity[0], entities)
  for entity_link in entity_uris:
    props_search = index_request("#propval", find_direct_prop_folder(entity_link), "subject", entity_link)
    reverse = False
    if props_search == []:
      props_search = index_request("#propval", find_reverse_prop_folder(entity_link), "subject", entity_link)
      reverse = True
    found_props_minus_brackets = [x.decode('utf-8')[1:-1] for x in props_search if len(x) > 2]
    found_props = interpret_prop_results(", ".join(found_props_minus_brackets))
    results = []
    for w in remaining_words_minus_stop_words:
      for [p1, v1] in found_props:
        if fuzz.ratio(shorten_prop(p1), w) > 85: # without "property/" and "ontology/"
          results.append(v1)
          for [p2, v2] in found_props:
            if p1 == p2 and v2 not in results:
              results.append(v2)
          if results != []:
            return (results, p1, reverse, entity_link)
          else:
            pass
    origin_props = try_origin_props(entity_link, words_without_question_words, all_words)
    if origin_props != ():
      return origin_props
    else:
      pass
  return ()
    
############################

def probably_simple_type(entities, properties, classes, words_without_question_words, all_words):
  if properties == [] and classes == []:
    return best_prop_in_simple_quest(entities, properties, classes, words_without_question_words, all_words)
  prop_ent_class_combination = best_prop_ent_class_combination(entities, properties, classes, words_without_question_words, False)
  if prop_ent_class_combination != []:
    for parse in prop_ent_class_combination[:20]: #[:3]:
      answer = categorise_parse_without_alternatives(parse, entities, properties, classes, words_without_question_words, False)
      if answer not in [(), []]:
        return answer
    if answer == ():
      answer = categorise_simple_parse(parse, entities, properties, classes, words_without_question_words, False)
      if answer not in [(), []]:
        return answer
      else:
        answer = try_all_combinations_of_props(parse, entities, properties, classes, words_without_question_words)
        if answer == ():
          answer = try_all_combinations_of_ents_and_props(entities, properties, words_without_question_words, all_words)
          return answer
        else:
          return answer
  else:
    parse = best_prop_ent_combination(entities, properties, classes, words_without_question_words)[0]
    return categorise_simple_parse(parse, entities, properties, classes, words_without_question_words, False)
  
def check_what_is_prop_of_ent(entities, properties, words_without_question_words):
  if properties != [] and properties[0][0] == 0:
    props = properties[0][1][1]
    props_index = 0
    words_remained = words_without_question_words[len(properties[0][1][0]):]
    if len(words_remained) > 1 and words_remained[0] == "of":
      words_remained = words_remained[1:]
      mathing_entity = [x for x in entities if x[1] == words_remained]
      if mathing_entity != []:
        entity = entity = "_".join(mathing_entity[0][1])
        ent_index = mathing_entity[0][0]
        answer = whatPropEnt(props, entity, props_index, ent_index, words_without_question_words, False, entities)
        if answer == ():
          return []
        else:
          return answer
      else:
        words_remained = [x.lower() for x in words_remained]
        mathing_entity = [x for x in entities if [a.lower() for a in x[1]] == words_remained]
        if mathing_entity != []:
          entity = entity = "_".join(mathing_entity[0][1])
          ent_index = mathing_entity[0][0]
          answer = whatPropEnt(props, entity, props_index, ent_index, words_without_question_words, False, entities)
          if answer == ():
            return []
          else:
            return answer
    else:
      return []
  else:
    return []
  
def find_question_type_and_answer(entities, properties, classes, words_without_question_words, all_words):
  if all_words[0].lower() in ["is", "are", "was", "were", "do", "does", "did"]:
    return yes_no_question(entities, properties, words_without_question_words, all_words)
  else:
    what_is_prop_of_ent = check_what_is_prop_of_ent(entities, properties, words_without_question_words)
    if what_is_prop_of_ent in [[], None]:
      independent_and = and_as_part_of_entity(entities, words_without_question_words) # check if it's a complex sentence with "and" or "which/that is/are also"
      complex_sentence_delimiter = delimiter_of_complex_sentence(words_without_question_words) 
      if independent_and != []:
        return complex_sentences(entities, properties, classes, words_without_question_words, all_words, independent_and[0], independent_and[0])
      elif complex_sentence_delimiter != ():
        return complex_sentences(entities, properties, classes, words_without_question_words, all_words, complex_sentence_delimiter[0], complex_sentence_delimiter[1])
      else:
        return probably_simple_type(entities, properties, classes, words_without_question_words, all_words)
    else:
      return what_is_prop_of_ent

############################

def make_sparql_triple_x(prop, reverse, ent):
  if isinstance(ent, (bytes, bytearray)):
    ent = ent.decode('utf-8')
  if reverse == False:
    return "<http://dbpedia.org/resource/" + ent + "> <http://dbpedia.org/" + prop + "> ?x"
  else:
    return "?x <http://dbpedia.org/" + prop + "> <http://dbpedia.org/resource/" + ent + ">"

def make_sparql_triple_uri(prop, reverse, ent):
  if isinstance(ent, (bytes, bytearray)):
    ent = ent.decode('utf-8')
  if reverse == False:
    return "<http://dbpedia.org/resource/" + ent + "> <http://dbpedia.org/" + prop + "> ?uri"
  else:
    return "?uri <http://dbpedia.org/" + prop + "> <http://dbpedia.org/resource/" + ent + ">"
    
def make_sparql_triple_x_uri(prop, reverse):
  if reverse == False:
    return "?x <http://dbpedia.org/" + prop + "> ?uri"
  else:
    return "?uri <http://dbpedia.org/" + prop + "> ?x"

def make_class_sparql_x(cl):
  return ". ?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/" + cl + ">}"

def make_class_sparql_uri(cl):
  return ". ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/" + cl + ">}"

############################
  
def process_quest(q):
  new_q = re.sub(r'( [A-Z]\.)([A-Z]\. )', r'\1 \2', q)
  all_words = new_q.split()
  (entities, properties, classes, words_without_question_words) = find_ents_props_classes(new_q)
  return find_question_type_and_answer(entities, properties, classes, words_without_question_words, all_words)
