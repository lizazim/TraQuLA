In revised evaluation, an answer is considered “correct” or “also possible” (i.e. semantically valid) if:

1) an output SPARQL query is completely the same as the gold standard query, or
2) an output SPARQL query produces the same values as the gold standard query, or
3) an output SPARQL query is semantically equivalent to the gold standard query, or
4) an output SPARQL query semantically corresponds to the input question, even though it might be semantically different from the gold standard query, or
5) an answer (set of answers) are the same as the one(s) that the gold standard query retrieves.

Some notes on groups 1–5:

1. A SPARQL query is considered completely the same as the gold standard query, if it operates with the same RDF triples and produces the same results. The order of triples in a query can vary:

*Tell me the name of the Prime Time Entertainment Network's TV show whose Artist is Christopher Franke ?*

Gold: SELECT DISTINCT ?uri WHERE {?uri <http://dbpedia.org/property/artist> <http://dbpedia.org/resource/Christopher_Franke> . ?uri <http://dbpedia.org/ontology/network> <http://dbpedia.org/resource/Prime_Time_Entertainment_Network>  . ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/TelevisionShow>}

Our: SELECT DISTINCT ?uri WHERE {?uri <http://dbpedia.org/ontology/network> <http://dbpedia.org/resource/Prime_Time_Entertainment_Network>. ?uri <http://dbpedia.org/property/artist> <http://dbpedia.org/resource/Christopher_Franke>. ?uri <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/TelevisionShow>}

2. If a SPARQL query retrieves the same output as the gold standard query, it is considered correct. Thus, if the system “understood” only a part of the question, but it was enough to output the correct value(s), the question is thought to be answered correctly. E.g.

*Who created the Women in the Garden and also the L'Enfant a la tasse ?*

Gold: SELECT DISTINCT ?uri WHERE { <http://dbpedia.org/resource/Women_in_the_Garden> <http://dbpedia.org/property/artist> ?uri. <http://dbpedia.org/resource/L'Enfant_a_la_tasse> <http://dbpedia.org/property/artist> ?uri . }

Our: SELECT DISTINCT ?uri WHERE {<http://dbpedia.org/resource/L'Enfant_a_la_tasse> <http://dbpedia.org/ontology/author> ?uri}

Result: http://dbpedia.org/resource/Claude_Monet

Sometimes the system outputs a query whose semantics is slightly incorrect. However, if the value(s) it retrieves coincide with the gold standard answer(s), we consider this answer correct:

*Who commanded the invasion of Buwat and made Fatima bint Sa'd famous?*

Gold: SELECT DISTINCT ?uri WHERE { <http://dbpedia.org/resource/Invasion_of_Buwat> <http://dbpedia.org/property/commander> ?uri. <http://dbpedia.org/resource/Fatimah_bint_Sa'd> <http://dbpedia.org/ontology/knownFor> ?uri . }

Our: SELECT DISTINCT ?uri WHERE {<http://dbpedia.org/resource/Invasion_of_Buwat> <http://dbpedia.org/property/commander> ?uri. <http://dbpedia.org/resource/Fatimah_bint_Asad> <http://dbpedia.org/ontology/knownFor> ?uri}

Result: http://dbpedia.org/resource/Muhammad

3. We consider two SPARQL queries as semantically equivalent, if the properties in them:

a) differ with “ontology/property” prefixes, e.g:

*Where can one find the Dzogchen Ponolop Rinpoche?*

Gold: SELECT DISTINCT ?uri WHERE { <http://dbpedia.org/resource/Dzogchen_Ponlop_Rinpoche> <http://dbpedia.org/property/location> ?uri }

Our: SELECT DISTINCT ?uri WHERE {<http://dbpedia.org/resource/Dzogchen_Ponlop_Rinpoche> <http://dbpedia.org/ontology/location> ?uri}

Judging by the training set, the “ontology/property” prefixes are used completely randomly. 

b) are synonyms (and can also have different “ontology/property” prefixes), e.g.:

*Where were sverre krogh sundbo and havard vad petersson born?*

Gold: SELECT DISTINCT ?uri WHERE { <http://dbpedia.org/resource/Sverre_Krogh_Sundbø> <http://dbpedia.org/property/birthPlace> ?uri. <http://dbpedia.org/resource/Håvard_Vad_Petersson> <http://dbpedia.org/property/placeOfBirth> ?uri}

Our: SELECT DISTINCT ?uri WHERE {<http://dbpedia.org/resource/Håvard_Vad_Petersson> <http://dbpedia.org/ontology/birthPlace> ?uri. <http://dbpedia.org/resource/Sverre_Krogh_Sundbø> <http://dbpedia.org/ontology/birthPlace> ?uri}

Judging by the training set, similar synonymous variations are also completely random. Sometimes they result into different sets of answers, but the system should not be punished for that. It is enough if the system produces a query that is semantically valid. 

In many cases the system chooses a better property out of the range of synonyms, which results into a more concise set of answers:

*Who all are known to play the Gibson Guitar Corporation?*

Gold: SELECT DISTINCT ?uri WHERE {?uri <http://dbpedia.org/property/notableInstruments> <http://dbpedia.org/resource/Gibson_Guitar_Corporation> } 

(retrieves 28 values)

Our: SELECT DISTINCT ?uri WHERE {?uri <http://dbpedia.org/ontology/instrument> <http://dbpedia.org/resource/Gibson_Guitar_Corporation>}

(retrieves 50 values)

If the system retrieves less answers, it shouldn’t be punished as well. Judging by the training set, there is no preference for properties producing more values. The system just has a task to produce anything sensible:

*How many things are written in C++?*

Gold: SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/property/programmingLanguage> <http://dbpedia.org/resource/C++>  . }
(retrieves 1003 values)

Our: SELECT DISTINCT COUNT(?uri) WHERE {?uri <http://dbpedia.org/property/writtenIn> <http://dbpedia.org/resource/C++>}
(retrieves 3 values)

The system has a list of synonymous properties, so in many cases it can automatically assess whether a replacement for a synonym was valid. But some cases are questionable and need a human to decide whether the output query is eligible, e.g.:

*To which places do the flights go by airlines headquartered in the UK?*

Gold: SELECT DISTINCT ?uri WHERE { ?x <http://dbpedia.org/property/headquarters> <http://dbpedia.org/resource/United_Kingdom> . ?x <http://dbpedia.org/property/destinations> ?uri  . ?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/Airline>}

Our: SELECT DISTINCT ?uri WHERE {?x <http://dbpedia.org/ontology/headquarter> <http://dbpedia.org/resource/United_Kingdom>. ?x <http://dbpedia.org/property/focusCities> ?uri. ?x <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://dbpedia.org/ontology/Airline>}

The properties “property/headquarters” and “ontology/headquarter” are undoubtedly synonymous. How about “destinations” and “focusCities”? They both denote “places to which some flights go”, even though these properties are not completely semantically equivalent. 

These controversial situations are collected in a list (*results/Possible_answers.txt*) and belong mostly to group 4 described below. 

4. Sometimes a question can be interpreted and answered in different ways, because:

a) The question contains ambiguous entities:

*Who directed The Haunted House ?* 

Gold: SELECT DISTINCT ?uri WHERE { <http://dbpedia.org/resource/The_Haunted_House_(1929_film)> <http://dbpedia.org/ontology/director> ?uri }

Our: SELECT DISTINCT ?uri WHERE { <http://dbpedia.org/resource/The_Haunted_House_(1921_film)> <http://dbpedia.org/ontology/director> ?uri }

b) The semantic entity-property relations within the questions can be understood in several ways:

*Which party has come in power in Mumbai North?*

Gold: SELECT DISTINCT ?uri WHERE { ?x <http://dbpedia.org/property/constituency> <http://dbpedia.org/resource/Mumbai_North_(Lok_Sabha_constituency)> . ?x <http://dbpedia.org/ontology/party> ?uri  . }

Our: SELECT DISTINCT ?uri WHERE {<http://dbpedia.org/resource/Mumbai_North_(Lok_Sabha_constituency)> <http://dbpedia.org/property/party> ?uri}

There are various cases in this subgroup, and they should be considered individually.
The system’s and gold standard answers were manually curated. We found some alternative semantically valid answers of the system (*results/Possible_answers.txt*) as well as some errors in the test split (*results/Errors_in_the_dataset.txt*).

5. This group includes all “Ask” (Boolean) questions: for some reason, all of them in the training and test sets are answered as “true”. In testing, the system just detected the Boolean type of the question and output “true”. This way of question answering is not valid enough, and we carry out separate evaluation, excluding the “Ask” questions from the test split (see the paper).
