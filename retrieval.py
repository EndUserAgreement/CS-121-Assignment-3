import sys
import json
from tkinter.tix import INTEGER
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


def lookup(input, exact):
    edited = input[len(exact) + 4:-3] # removes the word, beginning bracket, ending bracket, and newline from string
    #print(edited)
    find = edited.split(",") #splits everything into tuples in list
    for pair in find:
        check = pair.split(":")
        print(check)
        for num in check:
            print(num)
            #int(num)
    #print(find)


def getresults(input):
    words = [stemmer.stem(word) for word in word_tokenize(input.lower())]
    for word in words:
        first_letter = word[0]
        stemmedword = stemmer.stem(word)
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
    

    