# TraQuLA

TraQuLA is a a question answering (QA) system developed by means of linguistic analysis of datasets of complex questions over DBpedia. 

## Paper


## Requirements

* Python 3.6
* About 12.5 GB of disk space
* [PyLucene requirements](https://lucene.apache.org/pylucene/) 

## Installation

1. [Install PyLucene](https://lucene.apache.org/pylucene/).

2. Download dictionaries (from the Big Data server).

3. Write index. 

```bash
python setup.py
```

This step will take approx. 30 min.

## Run

To ask questions manually, run

```bash
python ask_your_question.py
```

and enter individual questions.

## Testing

The system was tested on the [LC-QuAD](https://github.com/AskNowQA/LC-QuAD) test split (1000 questions) by running

```bash
python lcquad_testing.py
```

We carry out “strict” and “revised” evaluation (*results/Results.txt*). In strict evaluation, we compare the output of the system with the gold standard, regardless of other possible ways to answer questions. In revised evaluation, if the output value(s) do(es) not coincide with the gold standard, the evaluation algorithm decides whether the output query is still semantically valid and if yes, assigns the micro precision and micro recall to 1. In revised evaluation, an answer is considered “correct” or “also possible” (i.e. semantically valid) if:

1) an output SPARQL query is completely the same as the gold standard query, or
2) an output SPARQL query produces the same values as the gold standard query, or
3) an output SPARQL query is semantically equivalent to the gold standard query, or
4) an output SPARQL query semantically corresponds to the input question, even though it might be semantically different from the gold standard query, or
5) an answer (set of answers) are the same as the one(s) that the gold standard query retrieves.

You can find comments on groups 1–5 in *results/Correctness_criteria.md*.

