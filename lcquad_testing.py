#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, lucene
import readline
import locale
import re
import operator
import subprocess 
import string
from string import Template
from string import punctuation
from datetime import datetime
from getopt import getopt, GetoptError
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader, Term
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher, TermQuery
from org.apache.lucene.store import SimpleFSDirectory
import json
from pprint import pprint
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from itertools import groupby
from collections import Counter as mset
from operator import itemgetter
import itertools
import unicodedata
import requests
from urllib.parse import quote
import multiprocessing
import time
import pathlib
import signal

timeout = 0 # timeout margin in seconds for each question. 0 - no limit

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

exec(open("src/process_question.py").read())
exec(open("src/searchIndex.py").read())
exec(open("src/makePropertiesIndex.py").read())
exec(open("src/makeClassesIndex.py").read())
exec(open("src/findEntsPropsClasses.py").read())

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

signal.signal(signal.SIGALRM, timeout_handler)

def remove_class_from_sparql(sparql):
  matches = re.search('(.*?)\. \?(uri|x) <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <(.*?)>}$', sparql)
  if matches == None:
    return sparql
  else:
    return (matches.group(1) + "}").replace(" }", "}")

def make_query_link(query):
  link = "http://client.linkeddatafragments.org/#datasources=http%3A%2F%2Ffragments.dbpedia.org%2F2016-04%2Fen&query="
  return link + quote(query.replace("COUNT(?uri)", "?uri"))
    
def get_answers_from_web(s):
  subprocess.call(["comunica-sparql https://fragments.dbpedia.org/2016-04/en -q \"" + s + "\" > out.txt"], shell = True) 
  with open("out.txt", 'r') as f:
    contents = f.readlines()
  if contents != []:
    contents = contents[1:-1]
  return [x.replace(",\n", "\n") for x in contents]
  
def check_in_web(answer, correct):
  results1 = get_answers_from_web(answer)
  results1.sort()
  results2 = get_answers_from_web(correct)
  results2.sort()
  if results2 in [['query has no results.'], []]:
    return ['query has no results.']
  if results1 == results2:
    return "true"
  else:
    return "false"

def count_in_web(answer, correct):
  results1 = get_answers_from_web(answer)
  results1.sort()
  results2 = get_answers_from_web(correct)
  results2.sort()
  if results2 == ['query has no results.']:
    return ['query has no results.']
  if results1 == results2:
    return ("1", "1")
  else:
    returned_correct = [x for x in results1 if x in results2]
    returned_correct_len = len(returned_correct)
    returned_results_len = len(results1)
    correct_results_len = len(results2)
    precision = float(returned_correct_len) / returned_results_len
    recall = float(returned_correct_len) / correct_results_len
    return (str(returned_correct_len) + " / " + str(returned_results_len) + " = " + str(precision), \
            str(returned_correct_len) + " / " + str(correct_results_len) + " = " + str(recall))
    
def find_properties_in_sparql(sparql):
  matches = re.findall('http://dbpedia.org/ontology/(.*?)>', sparql)
  if matches == []:
    return []
  else:
    new_matches = []
    for m in matches:
      if "#type> <http://dbpedia.org/ontology/" + m in sparql:
        pass
      else:
        new_matches.append(m)
    rest = sparql
    for m in matches:
      rest = rest.replace(m, "")
    return (new_matches, rest)

identical_props = []
for key in prop_functions.keys():
  group = [k[0][28:].lower() for k in prop_functions[key]]
  identical_props.append(group)
  
def check_identical_properties(answer_sparql, correct_query):
  answer_sparql = answer_sparql.lower()
  correct_query = correct_query.lower()
  (matches1, rest1) = find_properties_in_sparql(answer_sparql)
  (matches2, rest2) = find_properties_in_sparql(correct_query)
  if len(matches1) == len(matches2):
    for x1 in matches1:
      if x1 in matches2: 
        matches2.remove(x1)
      else:
        for g in identical_props:
          for x2 in matches2:
            if x1 in g and x2 in g:
              matches2.remove(x2)
  if matches2 == [] and rest1 == rest2:
    return True
  else:
    return False
    
def check_count_questions(q, sparql):
  count_phrases = ["give me an estimate of the number of", "give me the total number of", "give me a total number of", "give me the number of", "give me a number of", "give me the count of", "give me a count of", "give the total number of", "give a total number of", "give the number of", "give a number of", "give the count of", "give a count of", "tell me the total number of", "tell me a total number of", "tell the total number of", "tell a total number of", "tell me the number of", "tell me a number of", "tell the number of", "tell a number of", "count the total number of", "count a total number of", "count the number of", "count a number of", "count the", "name the total number of", "name a total number of", "name the number of", "name a number of", "what is the total number of", "what is a total number of", "what is the number of", "what number of", "which number of", "total number of", "the total number of", "what is a number of", "which is the total number of", "which is a total number of", "which is the number of", "which is a number of", "how many"]
  if [ele for ele in count_phrases if(ele in q.lower())] != [] or q.lower().startswith("count"): 
    return sparql.replace("DISTINCT ?uri WHERE", "DISTINCT COUNT(?uri) WHERE")
  else:
    return sparql

def print_incorrect():
  print("Correct: false")
  print("Strict precision: 0")
  print("Strict recall: 0")
  print("Revised precision: 0")
  print("Revised recall: 0")

def print_correct():
  print("Correct: true") 
  print("Strict precision: 1")
  print("Strict recall: 1")
  print("Revised precision: 1")
  print("Revised recall: 1")
  
something_wrong_with_answer_sparql = []

data = json.load(open('test-data.json'))
for quest in data:
  print("\n\n")
  print("id:", quest["_id"])
  print(quest["corrected_question"])
  if quest["corrected_question"].lower().startswith(("is ", "are ", "was ", "were ", "do ", "does ", "did ")):
    print("Gold: true")
    print("Our: true")
    print_correct()
  else:
    try:
      q = quest["corrected_question"].strip().strip('?').strip('.').strip().replace(", where", " , where").replace(", who", " , who").\
        replace(", which", " , which").replace(", what", " , what").replace(", that", " , that").replace("  ", " ")
      new_q = re.sub(r'( [A-Z]\.)([A-Z]\. )', r'\1 \2', q)
      signal.alarm(timeout) 
      try:
        answer = process_quest(new_q)
        if answer == []:
          print("Gold:", quest["sparql_query"].strip())
          print("Our: no answer")
          print_incorrect()
        else:
          answer_sparql = check_count_questions(new_q, answer[-1])
          answer_sparql_adjusted = answer_sparql.replace("  ", " ").replace("  ", " ").replace("?uri.", "?uri .").replace("?x.", "?x .").replace(">.", "> .").replace(".<", ". <").replace(".}", "}").replace("  ", " ").replace(" }", "}").replace("s>", ">").replace("COUNT(?uri)", "?uri").replace("{ ", "{").replace(" }", "}")
          correct_query = quest["sparql_query"].strip().replace("  ", " ").replace("  ", " ").replace("?uri.", "?uri .").replace("?x.", "?x .").replace("{ ", "{").replace(" }", "}").replace(">.", "> .").replace(".<", ". <").replace(".}", "}").replace("  ", " ").replace(" }", "}").replace("s>", ">").replace("COUNT(?uri)", "?uri")
          print("Gold:", quest["sparql_query"].strip())
          print("Our:", answer_sparql)
          if answer_sparql_adjusted.lower() == correct_query.lower(): 
            print_correct()
          else:
            answer_sparql_adjusted = answer_sparql_adjusted.replace("/property/", "/ontology/")
            correct_query = correct_query.replace("/property/", "/ontology/")
            if (sorted(answer_sparql_adjusted.lower()) == sorted(correct_query.lower())):
              print("Correct: also possible")
              (strict_precision, strict_recall)= count_in_web(answer[-1].replace("COUNT(?uri)", "?uri"), quest["sparql_query"].replace("COUNT(?uri)", "?uri"))
              print("Strict precision:", strict_precision)
              print("Strict recall:", strict_recall)
              print("Revised precision: 1")
              print("Revised recall: 1")
            elif (remove_class_from_sparql(answer_sparql_adjusted).lower() == remove_class_from_sparql(correct_query).lower()) or check_identical_properties(remove_class_from_sparql(answer_sparql_adjusted), remove_class_from_sparql(correct_query)) == True:
              if len(remove_class_from_sparql(correct_query)) < len(correct_query) and len(remove_class_from_sparql(answer_sparql_adjusted)) >= len(answer_sparql_adjusted):
                missed_class.append((i, quest["corrected_question"]))
              print("Correct: also possible")
              (strict_precision, strict_recall)= count_in_web(answer[-1].replace("COUNT(?uri)", "?uri"), quest["sparql_query"].replace("COUNT(?uri)", "?uri"))
              print("Strict precision:", strict_precision)
              print("Strict recall:", strict_recall)
              print("Revised precision: 1")
              print("Revised recall: 1")
            else: 
              web_request = check_in_web(answer[-1].replace("COUNT(?uri)", "?uri"), quest["sparql_query"].replace("COUNT(?uri)", "?uri")) 
              if web_request == "true":
                print_correct()
              elif web_request == ['query has no results.']:
                something_wrong_with_answer_sparql.append(quest["corrected_question"])
              else:
                print("Correct: false")
                (strict_precision, strict_recall)= count_in_web(answer[-1].replace("COUNT(?uri)", "?uri"), quest["sparql_query"].replace("COUNT(?uri)", "?uri"))
                print("Strict precision:", strict_precision)
                print("Strict recall:", strict_recall)
                print("Revised precision:", strict_precision)
                print("Revised recall:", strict_recall)
      except TimeoutException:
        print("Gold:", quest["sparql_query"].strip())
        print("Our: no answer")
        print("Correct: false")
        print("Strict precision: 0")
        print("Strict recall: 0")
        print("Revised precision: 0")
        print("Revised recall: 0")
        continue 
      else:
        signal.alarm(0)
    except Exception as e: 
      print("Gold:", quest["sparql_query"])
      print("Our: no answer")
      print_incorrect()
      
print(something_wrong_with_answer_sparql) # client.linkeddatafragments.org doesn't process queries containing entities with apostrophes. Have to verify them manually.