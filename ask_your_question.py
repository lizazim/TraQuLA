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

timeout = 60 # timeout margin in seconds for each question. 0 - no limit

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

def check_count_questions(q, sparql):
  count_phrases = ["give me an estimate of the number of", "give me the total number of", "give me a total number of", "give me the number of", "give me a number of", "give me the count of", "give me a count of", "give the total number of", "give a total number of", "give the number of", "give a number of", "give the count of", "give a count of", "tell me the total number of", "tell me a total number of", "tell the total number of", "tell a total number of", "tell me the number of", "tell me a number of", "tell the number of", "tell a number of", "count the total number of", "count a total number of", "count the number of", "count a number of", "count the", "name the total number of", "name a total number of", "name the number of", "name a number of", "what is the total number of", "what is a total number of", "what is the number of", "what number of", "which number of", "total number of", "the total number of", "what is a number of", "which is the total number of", "which is a total number of", "which is the number of", "which is a number of", "how many"]
  if [ele for ele in count_phrases if(ele in q.lower())] != [] or q.lower().startswith("count"): 
    return sparql.replace("DISTINCT ?uri WHERE", "DISTINCT COUNT(?uri) WHERE")
  else:
    return sparql

while True:
  print("\n\n")
  value = input("Ask something.\n")
  try:
    q = value.strip().strip('?').strip('.').strip().replace(", where", " , where").replace(", who", " , who").\
      replace(", which", " , which").replace(", what", " , what").replace(", that", " , that").replace("  ", " ")
    new_q = re.sub(r'( [A-Z]\.)([A-Z]\. )', r'\1 \2', q)
    signal.alarm(timeout) 
    try:
      answer = process_quest(new_q)
      if answer == []:
        print("No answer")
      else:
        answer_sparql = check_count_questions(new_q, answer[-1])
        print(answer[0])
        print(answer_sparql)
    except TimeoutException:
      print("No answer")
      continue 
    else:
      signal.alarm(0)
  except Exception as e: 
    print("No answer")