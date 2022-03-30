#!/usr/bin/env python3
# -*- coding: utf-8 -*-

path = pathlib.Path(__file__).parent.absolute() 

exec(open(str(path) + "/src/searchIndex.py").read())
exec(open(str(path) + "/src/makePropertiesIndex.py").read())
exec(open(str(path) + "/src/makeClassesIndex.py").read())
exec(open(str(path) + "/src/popular_props.py").read())

#lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def flat_list(l):
  return [item for sublist in l for item in sublist]

interchangeable_words = {"theatre" : ["theater"]}

def remove_duplicates_preserve_order(seq):
  seen = set()
  seen_add = seen.add
  return [x for x in seq if not (x in seen or seen_add(x))]
    
def sublist(ls1, ls2):
  def get_all_in(one, another):
    for element in one:
      if element in another:
        yield element
  for x1, x2 in zip(get_all_in(ls1, ls2), get_all_in(ls2, ls1)):
    if x1 != x2 and (x1 not in interchangeable_words[x2] or x2 not in interchangeable_words[x1]):
      return False
  return True

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

def merge_two_dicts(x, y):
  z = x.copy()
  z.update(y)
  return z

# -------------------------------
# Find entities

def interpret_candidates(candidates):
  if candidates == []:
    return []
  else:
    return flat_list([re.split('\', \'|\', "|", "|", \'', x.decode('utf-8')[2:-2]) for x in candidates])

unwanted = ["have been", "has been", "what is?", "name other", "i ny", "tv shows", "tv show", "tv series", "airlines", "actress", "the television", "member of the", "scientist", "the location", "companies", "airline", "the airline", "the scientists", "film star", "the film", "current", "kind", "thing", "things", "the things", "these things", "those things", "record labels", "mtv shows", "in thee", "how many", "given", "awards", "the awards", "spouse", "the insects", "places", "qtv shows", "currently", "the successor", "names", "names of", "is a", "where the", "in all", "one of them", "one of those", "one off", "the common", "all the things", "as one", "the one", "the ones", "there is", "there there"]

def analyse_entity_candidate(c, initial_c, word_index, hyphens_and_apostrophes_before_word, word, ws, original_words):
  c_words = c.split()
  c_words_initial = initial_c.split()
  new_word_index = word_index 
  if len(c_words) == 2 and c_words[1] == '\\\\':
    return []
  else:
    len_cand = len(c_words)
    first_word = c_words[0].lower()
    if first_word in ["a", "the"] and new_word_index != 0 and ws[new_word_index - 1].lower() == first_word:
      w_max_len = len(ws) - new_word_index + 1
    else:
      w_max_len = len(ws) - new_word_index
    if len_cand > w_max_len or c.lower() in unwanted or word in stop_words:
      return []
    else:
      if len_cand == 1:
        if c == initial_c:
          return [(word_index, c_words_initial, 100)]
        else:
          return [] 
      else:
        if first_word in ["a", "the"] and new_word_index != 0 and ws[new_word_index - 1].lower() == first_word:
          candidate_phrase = " ".join([w.lower() for w in ws[new_word_index - 1 : (new_word_index - 1 + len_cand)]]) 
          ratio = fuzz.ratio(candidate_phrase, c.lower())
          if ratio > 85:
            return [(word_index - 1, c_words_initial, ratio)]
          else:
            if len(ws) > new_word_index - 1 + len_cand: # in case of punctuation mismatches
              candidate_phrase = " ".join([w.lower() for w in ws[new_word_index - 1 : new_word_index + len_cand]])
              ratio = fuzz.ratio(candidate_phrase, c.lower())
              if ratio > 85:
                return [(word_index - 1, c_words_initial, ratio)]
            return []
        else:
          candidate_phrase = " ".join([w.lower() for w in ws[new_word_index : (new_word_index + len_cand)]])
          ratio = fuzz.ratio(candidate_phrase, c.lower())
          if ratio > 88:
            return [(word_index, c_words_initial, ratio)]
          else:
            if len(ws) > new_word_index + len_cand: # in case of punctuation mismatches
              candidate_phrase1 = " ".join([w.lower() for w in ws[new_word_index : (new_word_index + len_cand + 1)]])
              ratio1 = fuzz.ratio(candidate_phrase1, c.lower())
              if len(original_words) >= word_index + len_cand:
                candidate_phrase2 = " ".join([w.lower() for w in original_words[word_index: (word_index + len_cand)]])
                ratio2 = fuzz.ratio(candidate_phrase2, c.lower())
              else:
                ratio2 = 0
              if max([ratio1, ratio2]) > 88:
                return [(word_index, c_words_initial, max([ratio1, ratio2]))]
            return []
  
def match_candidates(ws, word, word_index, candidates):
  regex = re.compile('[%s]' % re.escape(string.punctuation)) 
  phrase_without_punctuation = regex.sub(' ', ' '.join(ws))
  original_words = ws[:]
  ws = phrase_without_punctuation.split()
  iter = re.finditer(r"\b( wasn t | weren t | isn t | aren t | don t | doesn t | didn t | won t | wouldn t | oughtn t | needn t | shouldn t | mustn t | can t | couldn t | haven t | hasn t | hadn t | shalln t | shan t | i m | it s | he s | she s | we re | you re | they re | i ve | you ve | they ve | we ve | i d | you d | she d | he d | it d | we d | they d | who d | who s | who ll | i ll | he ll | she ll | it ll | what s | mightn t | daren t | ain t | let s | o clock )\b", phrase_without_punctuation.lower())
  indices_and_matches = [(m.start(0), m.group()) for m in iter]
  for (i, m) in indices_and_matches:
    [s1, s2] = m.split()
    phrase_without_punctuation = phrase_without_punctuation[:i + len(s1) + 1] + "'" + phrase_without_punctuation[i + len(s1) + 2:]
  ws = phrase_without_punctuation.split()
  hyphens_and_apostrophes_before_word = sum([1 for x in original_words[:word_index] if "-" in x or "'" in x])
  matches_and_ratios = []
  for c in candidates:
    match = analyse_entity_candidate(c, c, word_index, hyphens_and_apostrophes_before_word, word, ws, original_words)
    if match != []:
      matches_and_ratios += match
    elif "(" in c:
      c_without_brackets = re.sub(r' \([^)]*\)', '', c)
      matches_and_ratios += analyse_entity_candidate(c_without_brackets, c, word_index, hyphens_and_apostrophes_before_word, word, ws, original_words)
  matches_and_ratios.sort(key = lambda x: len(x[1]), reverse = True)
  if len(matches_and_ratios) > 1:
    original_quest = " ".join(original_words)
    if matches_and_ratios[0][2] != 100:
      better_matching_non_one_word_cands = [x for x in matches_and_ratios[1:] if x[2] > matches_and_ratios[0][2] and len(x[1]) > 1]
      all_the_rest = matches_and_ratios[:]
      for x in better_matching_non_one_word_cands:
        all_the_rest.remove(x)
      matches_and_ratios = better_matching_non_one_word_cands + all_the_rest
    if "(" in " ".join(matches_and_ratios[0][1]) and "(" not in original_quest and matches_and_ratios[0][2] == 100: 
      ents_without_brackets = [(ind, lst, r) for (ind, lst, r) in matches_and_ratios if r == 100 and "(" not in " ".join(lst) and \
                               ((lst[0].lower() == "the" and len(lst) > 2) or (lst[0].lower() != "the" and len(lst) > 1))] 
      ents_without_brackets.sort(key = lambda x: len(x[1]), reverse = True)
      if ents_without_brackets != []:
        matches_and_ratios.remove(ents_without_brackets[0])
        matches_and_ratios = [ents_without_brackets[0]] + matches_and_ratios
    elif "(" in " ".join(matches_and_ratios[0][1]) and "(" in original_quest:
      ents_with_brackets = [(ind, lst, r) for (ind, lst, r) in matches_and_ratios if "(" in " ".join(lst)]
      best_ent = ()
      match_i = 0
      while best_ent == () and match_i < len(ents_with_brackets):
        (ind, lst, r) = ents_with_brackets[match_i]
        txt_without_punctuation = regex.sub(' ', ' '.join(lst))
        right_question_words_without_punctuation = regex.sub(' ', ' '.join(original_words[ind:]))
        if txt_without_punctuation == right_question_words_without_punctuation[:len(txt_without_punctuation)]:
          best_ent = (ind, lst, r)
          matches_and_ratios.remove(best_ent)
          matches_and_ratios = [best_ent] + matches_and_ratios
        match_i += 1
  if matches_and_ratios == []:
    matches = []
  else:
    matches_and_ratios.sort(key=lambda x: x[2], reverse = True)
    matches = matches_and_ratios[:5]
  return matches

def analyse_entity_candidate_by_2nd_word(c, initial_c, word_index, word, ws):
  c_words = c.split()
  c_words_initial = initial_c.split()
  len_cand = len(c_words)
  if len_cand == 2 and c_words[1] == '\\\\':
    return []
  elif len_cand == 1:
    return []
  else:
    first_word = c_words[0].lower()
    second_word = c_words[1].lower()
    if second_word == "of" and word_index == 1:
      return []
    else:
      if second_word == "of" and ws[word_index - 2].lower() == first_word and ws[word_index - 1].lower() == "of":
        w_max_len = len(ws) - word_index + 2
      else:
        w_max_len = len(ws) - word_index + 1
      if len_cand > w_max_len or c.lower() in unwanted:
        return []
      else:
        if second_word == "of" and ws[word_index - 2].lower() == first_word and ws[word_index - 1].lower() == "of":
          candidate_phrase = " ".join([w.lower() for w in ws[word_index - 2 : (word_index - 2 + len_cand)]]) 
          ratio = fuzz.ratio(candidate_phrase, c.lower())
          if ratio > 85:
            return [(c_words_initial, ratio)]
          else:
            return []
        else:
          candidate_phrase = " ".join([w.lower() for w in ws[word_index - 1 : (word_index - 1 + len_cand)]])
          ratio = fuzz.ratio(candidate_phrase, c.lower())
          if ratio > 88:
            return [(c_words_initial, ratio)]
          else:
            return []
            
def match_candidates_by_2nd_word(ws, word, word_index, candidates):
  if candidates == []:
    return []
  else:
    regex = re.compile('[%s]' % re.escape(string.punctuation)) 
    phrase_without_punctuation = regex.sub(' ', ' '.join(ws))
    ws = phrase_without_punctuation.split()
    matches_and_ratios = []
    for c in candidates:
      match = analyse_entity_candidate_by_2nd_word(c, c, word_index, word, ws)
      if match != []:
        matches_and_ratios += match
      elif "(" in c:
        c_without_brackets = re.sub(r' \([^)]*\)', '', c)
        matches_and_ratios += analyse_entity_candidate_by_2nd_word(c_without_brackets, c, word_index, word, ws)
    matches_and_ratios.sort(key = lambda x: len(x[0]), reverse = True)
    if matches_and_ratios != []:
      first_match_text = " ".join(matches_and_ratios[0][0])
      if "(" in first_match_text:
        first_match_text_before_brackets = re.sub(r' \([^)]*\)', '', first_match_text)
        first_place_element = []
        for x in matches_and_ratios[1:]:
          match_text = " ".join(x[0])
          if match_text == first_match_text_before_brackets:
            first_place_element = [x]
            matches_and_ratios.remove(x)
        matches_and_ratios = first_place_element + matches_and_ratios
    if matches_and_ratios == []:
      matches = []
    else:
      entities_with_of = []
      entities_without_of = []
      for m in matches_and_ratios[:5]:
        m_words = m[0]
        if len(m_words) > 1 and m_words[1].lower() == "of":
          entities_with_of.append(m)
        else:
          entities_without_of.append(m)
      if entities_with_of == []:
        matches = [(word_index - 1, x[0], x[1]) for x in entities_without_of]
      else:
        matches = [(word_index - 2, x[0], x[1]) for x in entities_with_of] + [(word_index - 1, x[0], x[1]) for x in entities_without_of]
    return matches
  
# -------------------------------
# Find properties

def match_properties(ws, word, word_index, candidates):
  if candidates == {}:
    return (word_index, [])
  else:
    matches_and_ratios = []
    for c in list(candidates):
      c_without_punctuation = c
      c_words_without_punctuation = c_without_punctuation.split()
      c_words = c.split()
      w_max_len = len(ws) - word_index
      len_cand = len(c_words_without_punctuation)
      if len_cand > w_max_len or c.lower() in class_and_prop_stop_phrases:
        pass
      else:
        if len_cand == 1 and word not in stop_words and c_without_punctuation.lower() not in class_and_prop_stop_phrases:
          matches_and_ratios.append(((c_words, candidates[c]), 100))
        elif len_cand > 1:
          ratio = fuzz.ratio(" ".join(ws[word_index:(word_index + len_cand)]).lower(), c_without_punctuation.lower())
          if ratio > 90:
            matches_and_ratios.append(((c_words, candidates[c]), ratio))
    if matches_and_ratios == []:
      return (word_index, [])
    else:
      matches_and_ratios.sort(key = lambda x: x[1], reverse = True)
      matches = [(c_words, cands) for ((c_words, cands), ratio) in matches_and_ratios[:5]] 
      return (word_index, matches)

# -------------------------------
# Find classes

def match_classes(ws, word, word_index, candidates):
  if candidates == {}:
    return (word_index, ())
  else:
    matches = []
    matches_and_ratios = []
    for c in list(candidates):
      c_without_punctuation = c
      c_words_without_punctuation = c_without_punctuation.split()
      c_words = c.split()
      w_max_len = len(ws) - word_index
      len_cand = len(c_words_without_punctuation)
      if len_cand > w_max_len or c.lower() in class_and_prop_stop_phrases:
        pass
      else:
        if len_cand == 1 and word not in stop_words and c_without_punctuation.lower() not in class_and_prop_stop_phrases:
          matches_and_ratios.append(((c_words, candidates[c]), 100))
        elif len_cand > 1:
          candidate_phrase = " ".join([w.lower() for w in ws[word_index:(word_index + len_cand)]])
          ratio = fuzz.ratio(candidate_phrase, c_without_punctuation)
          if ratio > 90:
            matches_and_ratios.append(((c_words, candidates[c]), ratio))
    if matches_and_ratios == []:
      return (word_index, ())
    else:
      max_ratio = max(matches_and_ratios, key = lambda item:item[1])[1]
      max_ratio_matches = [x for x in matches_and_ratios if x[1] == max_ratio]
      best_match = max(max_ratio_matches, key = lambda item:len(item[0][0]))[0]
      matches.append(best_match)
    if len(matches) > 1:
      matches.sort(key=lambda x: (-len(x[0]), x))
      longest_len = len(matches[0][0])
      matches = [x for x in matches if len(x[0]) == longest_len][0]
    return (word_index, matches[0])

# -------------------------------
# Delete entities coinciding with classes

def preceeded_by_question_words(i_e, words):
  words = [w.lower() for w in words]
  one_word = ["some", "name", "list", "different", "what", "which", "whose"]
  two_words = [["what", "is"], ["what", "are"], ["name", "the"], ["name", "a"], ["list", "the"], ["list", "a"], ["how", "many"]]
  three_words = [["what", "is", "the"], ["what", "are", "the"], ["what", "is", "a"], ["what", "are", "a"], ["what", "is", "an"], \
                 ["what", "are", "an"], ["who", "is", "the"], ["who", "are", "the"], ["who", "is", "a"], ["who", "are", "a"], \
                 ["who", "is", "an"], ["who", "are", "an"]]
  if (i_e >= 1 and words[i_e - 1] in one_word) or \
     (i_e >= 2 and words[i_e - 2 : i_e] in two_words) or \
     (i_e >= 3 and words[i_e - 3 : i_e] in three_words):
    return True
  else:
    return False

# -------------------------------
# Arrange entities, paroperties and classes by length (longest first)
  
def arrange_entities(entities):
  new_entities = []
  for (i, ents) in entities:
    entities_with_scores = []
    for e in ents:
      score = len(e)
      entities_with_scores.append((e, score))
    entities_with_scores.sort(key = lambda x: x[1], reverse = True)
    entities_without_scores = [e for (e, s) in entities_with_scores]
    new_entities.append((i, entities_without_scores))
  return new_entities

def arrange_properties(properties):
  new_properties = []
  for (i, props) in properties:
    properties_with_scores = []
    for (prop_words, prop_functions) in props:
      score = len(prop_words)
      properties_with_scores.append(((prop_words, prop_functions), score))
    properties_with_scores.sort(key = lambda x: x[1], reverse = True)
    properties_without_scores = [p for (p, s) in properties_with_scores]
    new_properties.append((i, properties_without_scores))
  return new_properties
  
stop_words = ['a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', 'couldn', "couldn't", 'd', 'did', 'didn', "didn't", 'do', 'does', 'doesn', "doesn't", 'doing', 'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven', "haven't", 'having', 'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is', 'isn', "isn't", 'it', "it's", 'its', 'itself', 'just', 'll', 'm', 'ma', 'me', 'mightn', "mightn't", 'more', 'most', 'mustn', "mustn't", 'my', 'myself', 'needn', "needn't", 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shan', "shan't", 'she', "she's", 'should', "should've", 'shouldn', "shouldn't", 'so', 'some', 'such', 't', 'than', 'that', "that'll", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 'wasn', "wasn't", 'we', 'were', 'weren', "weren't", 'what', 'when', 'where', 'which', 'while', 'who', 'whom', 'whose', 'why', 'will', 'with', 'won', "won't", 'wouldn', "wouldn't", 'y', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', 'named', 'also', 'different', 'someone', 'tv', 'one']

class_and_prop_stop_phrases = ["have been", "has been", "what is?", "name other"]

# -------------------------------
# Finding entities, props and classes for every word

def delete_ents(entity_matches, to_delete):
  new_entity_matches = []
  for (i, ents) in entity_matches:
    for e in ents:
      if (i, e) in to_delete:
        pass
      else:
        new_entity_matches.append((i, e))
  return [(k, list(list(zip(*g))[1])) for k, g in groupby(new_entity_matches, itemgetter(0))]

def delete_props(property_matches, to_delete):
  new_property_matches = []
  for (i, props) in property_matches:
    for (prop_words, prop_functions) in props:
      if (i, [(prop_words, prop_functions)]) in to_delete:
        pass
      else:
        new_property_matches.append((i, (prop_words, prop_functions)))
  return [(k, list(list(zip(*g))[1])) for k, g in groupby(new_property_matches, itemgetter(0))]

def remove_ratios(all_entity_matches):
  new_entity_matches = []
  for (i, ents) in all_entity_matches:
    new_ents = [e[0] for e in ents]
    new_entity_matches.append((i, new_ents))
  return new_entity_matches

def index_to_each_element(elements):
  new_elements = []
  for (i, els) in elements:
    for e in els:
      new_elements.append((i, e))
  return new_elements

def find_substr(s, char):
  index = 0
  if char in s:
    c = char[0]
    for ch in s:
      if ch == c:
        if s[index : index + len(char)] == char:
          return index
      index += 1
  return -1
    
def find_question_word(q):
  question_phrases = ["give me an estimate of the number of", "give me the total number of", "give me a total number of", "give me the number of", "give me a number of", "give me the count of", "give me a count of", "give the total number of", "give a total number of", "give the number of", "give a number of", "give the count of", "give a count of", "give me", "give the", "give", "list the", "list", "tell me the total number of", "tell me a total number of", "tell the total number of", "tell a total number of", "tell me the number of", "tell me a number of", "tell the number of", "tell a number of", "tell me", "tell the", "tell", "count the total number of", "count a total number of", "count the number of", "count a number of", "count the", "count", "name the total number of", "name a total number of", "name the number of", "name a number of", "name the", "name", "what is the", "what is the total number of", "what is a total number of", "what is the number of", "what number of", "which number of", "total number of", "the total number of", "what is a number of", "what is", "what", "which is the total number of", "which is a total number of", "which is the number of", "which is a number of", "which is the", "which is", "which", "in which", "in what", "who all" , "who", "how many", "is", "are", "do", "does", "did", "was", "were", "where", "where is", "where are", "where was", "where were", "where does", "where do", "where did", "where can i find", "where can one find", "when"] 
  q_lower = q.lower()
  potential_question_words = []
  for x in question_phrases:
    index = find_substr(q_lower, x)
    if index != -1:
      if (index != 0 and q_lower[index - 1].isalpha()) or (len(q) > index + len(x) and q_lower[index + len(x)].isalpha()): # to avoid removing "tell" from "Bertello"
        pass
      else:
        potential_question_words.append((x, index))
  if potential_question_words == []:
    return ([], 0)
  else:
    potential_question_words.sort(key = lambda x: x[1])
    first_index = potential_question_words[0][1]
    same_index = [x for x in potential_question_words if x[1] == first_index]
    same_index.sort(key = lambda x: len(x[0]), reverse = True)
    return same_index[0]

def entity_candidates_request(folder, w):
  candidates = index_request("#value", folder, "subject", w)
  if candidates == []:
    candidates = index_request("#value", folder, "subject", w + "_SPLITSUBJECT1")
    if candidates != []:
      x = 2
      new_cands = index_request("#value", folder, "subject", w + "_SPLITSUBJECT" + str(x))
      candidates += new_cands
      while new_cands != []:
        x += 1
        new_cands = index_request("#value", folder, "subject", w + "_SPLITSUBJECT" + str(x))
        candidates += new_cands
  return interpret_candidates(candidates)
  
def find_entity_candidates(folder, w):
  candidates = entity_candidates_request(folder, w)
  if len(w) > 1 and w[-1].isalpha() == False: 
    w = w[:-1]
    new_candidates = entity_candidates_request(folder, w)
    candidates += new_candidates
  return candidates

def find_property_or_class_candidates(w, dictionary):
  if w in dictionary:
    candidates = dictionary[w]
  else:
    candidates = {}
  if w.endswith("'s"):
    w_without_apostrophe = w[:-2]
    if w_without_apostrophe in dictionary:
      candidates = merge_two_dicts(candidates, dictionary[w_without_apostrophe])
  if w.endswith("s"):
    if w[:-1] in dictionary:
      candidates = merge_two_dicts(candidates, dictionary[w[:-1]])
    if len(w) > 3 and w[:-3] + "y" in dictionary:
      candidates = merge_two_dicts(candidates, dictionary[w[:-3] + "y"])
  return candidates

def match_popular_properties(words, w, word_index):
  result = []
  if w not in stop_words:
    for k in popular_props:
      k_words = k.split()
      len_k = len(k_words)
      if len(words) >= len_k + word_index:
        text_phrase_words = words[word_index:word_index+len_k]
        text_phrase = " ".join(text_phrase_words).lower()
        if text_phrase not in class_and_prop_stop_phrases:
          if 89 < fuzz.ratio(text_phrase, k) < 100:
            if k_words[0] in properties_dict:
              if k in properties_dict[k_words[0]]:
                candidates = properties_dict[k_words[0]][k]
                result.append((text_phrase_words, candidates))
  if result == []:
    return ()
  else:
    return (word_index, result)
  
def find_ents_props_classes(q):
  word_index = 0
  all_entity_matches = []
  all_property_matches = []
  all_class_matches = []
  (question_words, question_words_index) = find_question_word(q)
  q_without_question_words = q[:question_words_index] + q[question_words_index + len(question_words):]
  words = q_without_question_words.split()
  for w in words:
    w = w.lower()
    if w[-1].isalpha() == False and is_number(w) == False and len(w) > 1:
      w = w[:-1]
    if w in ["what", "which", "list", "name", "who", "whom", "whose"]:
      word_index += 1
    else:
      if len(w) == 1 or w[:2].isalpha() == False:
        folder = "other"
      else:
        folder = w[:2]
      candidates_1st_word = find_entity_candidates("labelsindex/" + folder, w)
      if word_index == 0:
        candidates_2nd_word = []
      else:
        candidates_2nd_word = find_entity_candidates("labels2ndword/" + folder, w)
      matches1 = match_candidates(words, w, word_index, candidates_1st_word)
      matches2 = match_candidates_by_2nd_word(words, w, word_index, candidates_2nd_word)
      matches = matches1 + matches2
      property_candidates = find_property_or_class_candidates(w, properties_dict)
      class_candidates = find_property_or_class_candidates(w, classes_dict)
      property_matches = match_properties(words, w, word_index, property_candidates)
      class_matches = match_classes(words, w, word_index, class_candidates)
      all_entity_matches += matches
      if property_matches[1] != []:
        all_property_matches.append(property_matches)
      else:
        popular_property_matches = match_popular_properties(words, w, word_index)
        if popular_property_matches != ():
          all_property_matches.append(popular_property_matches)
      if class_matches[1] != ():
        all_class_matches.append(class_matches)
      word_index += 1
  all_entity_matches = [(i, lst) for (i, lst, r) in all_entity_matches]
  all_entity_matches.sort(key = lambda x: len(x[1]), reverse = True)
  all_property_matches = index_to_each_element(all_property_matches)
  return (remove_duplicates_preserve_order_in_ents(all_entity_matches), all_property_matches, all_class_matches, words)

def remove_duplicates_preserve_order_in_ents(seq):
  seq = [(i, tuple(e)) for (i, e) in seq]
  seen = set()
  seen_add = seen.add
  no_duplicates = [x for x in seq if not (x in seen or seen_add(x))]
  return [(i, list(e)) for (i, e) in no_duplicates]
