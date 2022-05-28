import sys
import json
# from tkinter.tix import INTEGER 
import requests
import json #
import os#
import re#
import math#
import lxml#
import pprint #
import nltk
import time
from nltk.corpus import stopwords
from urllib import request
from pathlib import Path
from nltk.stem.snowball import SnowballStemmer#
from bs4 import BeautifulSoup#
from collections import defaultdict
from nltk.tokenize import word_tokenize

"""
CHANGES MADE:
- commented out tkinter import
- downloaded 'punkt' from nltk because I was prompted to in order to run the file
- prints out performance speed in milliseconds after query
- 
"""

stemmer = SnowballStemmer(language="english")
doc_ids = None
doc_ids_path = "/mnt/c/users/paolo/code/UCI/CS121/CS-121-Assignment-3/indexes/doc_id.txt" # Update the path to doc_id.txt, if necessary
NUM_DOCUMENTS = 55393

with open(doc_ids_path, "r") as text: 
    line = text.readline()
    doc_ids = eval(line)
total_docs = len(doc_ids)


def get_posting(input, exact):
    edited = input[len(exact) + 4:-3] # removes the word, beginning bracket, ending bracket, and newline from string
    find = edited.split(",") #splits everything into tuples in list
    posting = {int(str_pair.split(":")[0]):float(str_pair.split(":")[1]) for str_pair in find} # convert posting string to a posting dictionary with doc id as key and tf as value
    return posting # return posting


def get_results(input):
    """Using the lnc.ltc to ranks scores"""

    query_vector = defaultdict(int)
    document_vectors = defaultdict(dict)
    scores = defaultdict(float)

    words = [stemmer.stem(word) for word in word_tokenize(input.lower())]
    for word in words:

        # Calculate posting for particular search word
        first_letter = word[0]
        stemmedword = stemmer.stem(word)
        posting = parse_index(first_letter, stemmedword) 

        # Calculate tf-idf for particular search word in input search query
        query_tf_raw = words.count(word) # raw term frequency (tf) for word
        query_tf_wt = math.log(query_tf_raw) + 1 # tf-weighted for word
        query_idf = NUM_DOCUMENTS / math.log(len(posting)) # idf for word 
        query_tfidf = round(query_tf_wt * query_idf, 4) 
        query_vector[word] = query_tfidf

        for doc_id, tf in posting.items():
            document_vectors[doc_id][word] = tf

    # Normalize vectors
    query_vector_length = math.sqrt(sum(list(map(lambda x:x**2, query_vector.values()))))
    normalized_query_vector = {word:(tfidf/query_vector_length) for word, tfidf in query_vector.items()}
    normalized_document_vectors = defaultdict(dict)
    for doc_id, doc_vector in document_vectors.items():
        doc_vector_length = math.sqrt(sum(list(map(lambda x:x**2, doc_vector.values()))))
        for word in doc_vector.keys():
            normalized_document_vectors[doc_id][word] = document_vectors[doc_id][word]/doc_vector_length

    
    # Calculate cosine scores by performing dot product of each query vector to each document vector
    for doc_id, doc_vector in normalized_document_vectors.items():
        
        for word, norm_tfidf in normalized_query_vector.items():
            scores[doc_id] += norm_tfidf * doc_vector[word] if word in doc_vector.keys() else 0.0

    # print(query_vector)
    # print(normalized_query_vector)
    # # print(document_vectors)
    # print(normalized_document_vectors)
    # print(scores)
    return scores


def parse_index(letter, word):
    # index_file = r"C:\Users\srb71\Documents\GitHub\CS-121-Assignment-3\indexes\index" + letter + ".txt"   SHOB'S path
    index_file = "/mnt/c/users/paolo/code/UCI/CS121/CS-121-Assignment-3/indexes/index" + letter + ".txt"
    with open(index_file, "r", encoding="utf-8") as readfile:
        #js = json.loads(readfile.read())
        exact = "\"" + word + "\""
        for entry in readfile:
            if exact in entry:
                # print(entry)
                return get_posting(entry, exact) # return posting if found
        
        return {} # returns empty posting if not found in inverted index

if __name__ == "__main__":
    query = input("Input Search Query: ")
    start_time = time.process_time() * 1000 # start time in milliseconds
    print("Generating results for " + query)
    # Get index
    get_results(query)
    end_time = time.process_time() * 1000 # ending time in milliseconds
    print("Elapsed time (ms):", end_time - start_time)   # performance speeds needs to be < 300 ms
    index_file = "/mnt/c/users/paolo/code/UCI/CS121/CS-121-Assignment-3/urls.json" # Update the path to urls.json, if necessary
    with open(index_file, "r") as json_file:
        index = json.load(json_file)
    

    