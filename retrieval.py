import sys
import json
import requests
import json #
import os#
import re#
import math#
import lxml#
import pprint #
from nltk.corpus import stopwords
from urllib import request
from pathlib import Path
from nltk.stem.snowball import SnowballStemmer#
from bs4 import BeautifulSoup#
from collections import defaultdict
from nltk.tokenize import word_tokenize


stemmer = SnowballStemmer(language="english")
doc_ids = None

with open(r"C:\Users\srb71\Documents\GitHub\CS-121-Assignment-3\indexes\doc_id.txt") as text:
    line = text.readline()
    doc_ids = eval(line)
total_docs = len(doc_ids)
'''
def merge(posting1: list[list], posting2: list[list]):
    """Finds the intersection of post_ids between two list of postings"""

    p1 = set([p[0] for p in posting1])
    p2 = set([p[0] for p in posting2])
    return p1.intersection(p2)

def merge_multiple(index, *search_words):
    """Finds intersection for two or more list of postings, given the search words"""

    if len(search_words) == 1:
        return merge(index[search_words[0]], index[search_words[0]])

    merged_posting = merge(index[search_words[0]], index[search_words[1]])
    search_words = search_words[2:]

    while len(search_words) >= 1:  
        merged_posting.intersection(merge(index[search_words[0]], index[search_words[0]]))
        search_words = search_words[1:]

    return merged_posting

def get_top_doc_ids(search_words: list, doc: set):
    """Gets the top document_ids based on document frequency of search words"""

    result = defaultdict(int)

    for list_of_postings in search_words:

        for doc_id in doc:

            for posting in list_of_postings:

                if posting[0] == doc_id:
                    
                    result[doc_id] += posting[1]

    return sorted(result.items(), key=lambda x: x[1], reverse=True)


def get_top_urls(top_doc_ids: list[tuple], urls: list) -> list[tuple]:
    """Returns the top urls"""

    top_urls = list()

    for pair in top_doc_ids:
        if requests.get(urls[pair[0]]).status_code == 200:
            top_urls.append((urls[pair[0]], pair[1]))

        if len(top_urls) == 5:
            break

    return top_urls
'''
def lookup(input, exact):
    edited = input[len(exact) + 4:-3] # removes the word, beginning bracket, ending bracket, and newline from string
    #print(edited)
    find = edited.split(",") #splits everything into tuples in list
    for pair in find:
        check = pair.split(":")
        print(check)
        for num in check:
            print(num)
    #print(find)


def getresults(input):
    words = [stemmer.stem(word) for word in word_tokenize(input.lower())]
    for word in words:
        first_letter = input[0]
        stemmedword = stemmer.stem(input)
        getindex(first_letter, stemmedword)
    

def getindex(letter, word):
    index_file = r"C:\Users\srb71\Documents\GitHub\CS-121-Assignment-3\indexes\index" + letter + ".txt"
    with open(index_file, "r", encoding="utf-8") as readfile:
        #js = json.loads(readfile.read())
        exact = "\"" + word + "\""
        for entry in readfile:
            if exact in entry:
                print(entry)
                lookup(entry, exact)

if __name__ == "__main__":
    query = input("Input Search Query: ")
    print("Generating results for " + query)
    # Get index
    getresults(query)
    index_file = "C:/Users/srb71/Documents/GitHub/CS-121-Assignment-3/urls.json"
    with open(index_file, "r") as json_file:
        index = json.load(json_file)
    

    