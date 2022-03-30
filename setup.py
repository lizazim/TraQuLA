#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import bz2, os, re
import lucene
import sys
import string
from subprocess import *
from os import listdir
from os.path import isfile, join

from string import Template
from getopt import getopt, GetoptError
from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import KeywordAnalyzer 
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.store import SimpleFSDirectory
import pickle
import zipfile
import pathlib
import shutil

def split_lst(arr, size):
  arrs = []
  while len(arr) > size:
    pice = arr[:size]
    arrs.append(pice)
    arr   = arr[size:]
  arrs.append(arr)
  return arrs

def smaller_parts(current_parts):
  final_parts = []
  count = 0
  for x in current_parts:
    if sys.getsizeof(str(x)) > 32766:
      part1 = x[:int(len(x)/2)]
      part2 = x[int(len(x)/2):]
      final_parts.append(part1)
      final_parts.append(part2)
      count += 1
    else:
      final_parts.append(x)
  if count == 0:
    return current_parts
  else:
    return smaller_parts(final_parts)

path = pathlib.Path(__file__).parent.absolute()
dicts_path = str(path) + "/dicts"
extension = ".zip"

def unpack_file(f):
  file_name = os.path.abspath(f) 
  zip_ref = zipfile.ZipFile(file_name) 
  zip_ref.extractall(str(path) + "/unzipped") 
  zip_ref.close()

def move_files(source_folder, target_folder):
  source = str(path) + "/unzipped/" + source_folder
  files = os.listdir(source)
  for f in files:
    shutil.move(source + f, str(path) + target_folder)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def write_index(source_file, index_folder, field1, field2):
  directory = SimpleFSDirectory(Paths.get('./index/' + index_folder))
  analyzer = KeywordAnalyzer()
  config = IndexWriterConfig(analyzer)
  writer = IndexWriter(directory, config)
  with open(source_file, 'rb') as handle:
    diction = pickle.load(handle, encoding = 'utf8')
    for k in list(diction):
      partitioned_value = smaller_parts([diction[k]])
      if len(partitioned_value) == 1:
        pass
      else:
        for s in range(len(partitioned_value)):
          diction[k + "_SPLITSUBJECT" + str(s + 1)] = partitioned_value[s]
        del diction[k]
    for k in list(diction):
      doc = Document()
      doc.add(Field(field1, k, StringField.TYPE_STORED))
      doc.add(Field(field2, str(diction[k]), StringField.TYPE_STORED))
      try:
        writer.addDocument(doc)
      except:
        pass
    writer.commit()
    writer.close()

def write_indexes(source_folder, index_folder, field1, field2):
  full_source = './unzipped/' + source_folder
  files = [f for f in listdir(full_source) if isfile(join(full_source, f)) and f.endswith(".pkl")]
  for f in files:
    source_file = full_source + f
    index_name = re.sub(r'^.*?_', '', f)[:-4]
    write_index(source_file, index_folder + index_name, field1, field2)

print("Writing labels...")
for f in ["dicts/labelIndex1.zip", "dicts/labelIndex2.zip", "dicts/labelIndex3.zip"]:
  unpack_file(f)
for folder in ["labelIndex2/", "labelIndex3/"]:
  move_files(folder, "/unzipped/labelIndex1")
write_indexes("labelIndex1/", "labelsindex/", "subject", "value")
shutil.rmtree('unzipped')
for f in ["dicts/labelIndex2ndWord1.zip", "dicts/labelIndex2ndWord2.zip", "dicts/labelIndex2ndWord3.zip"]:
  unpack_file(f)
for folder in ["labelIndex2ndWord2/", "labelIndex2ndWord3/"]:
  move_files(folder, "/unzipped/labelIndex2ndWord1")
write_indexes("labelIndex2ndWord1/", "labels2ndword/", "subject", "value")
shutil.rmtree('unzipped')
print("Writing properties...")
for f in ["dicts/properties1.zip", "dicts/properties2.zip", "dicts/properties3.zip"]:
  unpack_file(f)
for folder in ["properties2/", "properties3/"]:
  move_files(folder, "/unzipped/properties1")
write_indexes("properties1/", "propertiesindex/", "subject", "propval")
shutil.rmtree('unzipped')
print("Writing reverse properties...")
for f in ["dicts/propreverse1.zip", "dicts/propreverse2.zip", "dicts/propreverse3.zip"]:
  unpack_file(f)
for folder in ["propreverse2/", "propreverse3/"]:
  move_files(folder, "/unzipped/propreverse1")
write_indexes("propreverse1/", "propertiesIndexReverse/", "subject", "propval")
shutil.rmtree('unzipped')
print("Writing disambiguations...")
unpack_file("dicts/disambiguations.zip")
write_indexes("disambiguations/", "disambiguations/", "subject", "value")
shutil.rmtree('unzipped')
print("Writing redirects...")
for f in ["dicts/redirects1.zip", "dicts/redirects2.zip", "dicts/redirects3.zip"]:
  unpack_file(f)
for folder in ["redirects2/", "redirects3/"]:
  move_files(folder, "/unzipped/redirects1")
write_indexes("redirects1/", "redirectsindex/", "subject", "value")
shutil.rmtree('unzipped')
print("Writing instance types...")
for f in ["dicts/instanceTypes1.zip", "dicts/instanceTypes2.zip", "dicts/instanceTypes3.zip"]:
  unpack_file(f)
for folder in ["instanceTypes2/", "instanceTypes3/"]:
  move_files(folder, "/unzipped/instanceTypes1")
write_indexes("instanceTypes1/", "instanceTypes/", "subject", "value")
shutil.rmtree('unzipped')