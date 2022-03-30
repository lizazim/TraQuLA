#!/usr/bin/env python3
# -*- coding: utf-8 -*-

path = pathlib.Path(__file__).parent.absolute() 

class CustomTemplate(Template):
    delimiter = '#'
    
def index_request(format, dir, record_name, query):
  path = pathlib.Path(__file__).parent.absolute() 
  indexDir = str(path) + '/index/' + dir
  template = CustomTemplate(format)
  fsDir = SimpleFSDirectory(Paths.get(indexDir))
  reader = DirectoryReader.open(fsDir)
  searcher = IndexSearcher(reader)
  query = TermQuery(Term(record_name, query))
  scoreDocs = searcher.search(query, 10000000000).scoreDocs
  results = []
  for scoreDoc in scoreDocs:
    doc = searcher.doc(scoreDoc.doc)
    table = dict((field.name(), field.stringValue())
                   for field in doc.getFields())
    results.append(template.substitute(table).encode('utf-8'))
  reader.close()
  return results
