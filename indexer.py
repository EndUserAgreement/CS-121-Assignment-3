import sys
import json
import os
import re
import nltk
import math
import lxml
import pprint
from urllib import request
from pathlib import Path
from nltk.stem.snowball import SnowballStemmer
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.tokenize import RegexpTokenizer, sent_tokenize, word_tokenize
from requests import head

nltk.download('punkt')
#from simhash import Simhash, SimhashIndex       #from https://github.com/leonsim/simhash     CHECK THIS

#LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ""]
#letterhold = defaultdict(letters)
docID=[]
invertedIndex = {}
#hashed = SimhashIndex([], k=1)
stemmer = SnowballStemmer(language="english")
#INVERSE INDEX
# TODO: keep track of when to write to disc
# TODO: merging and writing to disc
# TODO: how to organize inverted index for better merging
# TODO: what data structure for inverse index

#QUERY FUNCTIONS
# TODO: Query searching
# TODO: tf-idf function

""" 
class Posting:
    def __init__(self, docid, tfidf, fields):
        self.docid = docid
        self.tfidf = tfidf # use freq counts for now
        self.fields = fields
"""
 

#parse through the json file and extract all words, return whole doc as one large string
def parse_json(path):
    with open(path, "r") as read_file:
        file = json.load(read_file)
    soup = BeautifulSoup(file["content"], "lxml")
    for word in soup.find_all(['script', 'style']):
        word.extract()
    content = soup.get_text(" ")

    headers = soup.find_all(['h1', 'h2', 'h3', 'b', 'a'], text=True)
    headers = ' '.join([e.string for e in headers])
    return content + " " + headers


 #Returns a list of tf-ids for each word in document
def process_tfid(document: str):
    document = word_tokenize(document.lower().replace('\\',''))
    stemmed = [stemmer.stem(word) for word in document]
    tfids = {}
    for word in stemmed:
        if word in tfids: 
            tfids[word] += 1
        else: 
            tfids[word] = 1
    for word in tfids:
        tfids[word] = math.log(tfids[word]) + 1
    return tfids

#assigns the tf scores to the document w/ the doc_id, then puts it into the index
def combine(tf: dict, doc_id: int):
    for word in tf:
        if word in invertedIndex:
            invertedIndex[word][doc_id] = tf[word]
        else:
            invertedIndex[word] = {doc_id: tf[word]}


def processFolder(path):
    print(path) # remove later
    #doc = parse_json(path)
    #temp = process_tfid(doc)
    os.chdir(os.getcwd() + "/" + path) # go into the folder and set it to directory
    for site in os.listdir(os.getcwd()):
        current_doc = len(docID)
        docID.append({'id': current_doc, 'url': path + '/' + site})
        word_file = parse_json(site)
        #simhash_words = Simhash(word_file) #FIX THIS UP
        #if len(hashed.get_near_dups(simhash_words)) <= 0:
            #hashed.add(site, simhash_words)
        tf_dict = process_tfid(word_file) # was indented
        combine(tf_dict, docID) #was indented
    os.chdir('..') #leave the current directory

        
def process():
    os.chdir(r"C:\Users\srb71\Documents\CS121 Test Data\ANALYST")
    index_count = 1
    for f in os.listdir(os.getcwd()):
        if os.path.isdir(f):
            processFolder(f)
        if len(invertedIndex>200000):
            writeToFile(index_count)
            index_count += 1
    if len(invertedIndex) > 0:
        writeToFile(index_count)

def writeToFile(count: int):
    with open(r"C:\Users\srb71\Documents\GitHub\CS-121-Assignment-3\indexes" + str(count) + ".txt", "w") as file:
        file.write(str(invertedIndex))
    clean_print()
    invertedIndex.clear()


def createIndex():
    #index_count = 1
    #DELETION
    #while(os.path.exists("indexes/partial_index"))
    process()
    os.chdir("..")

    with open(r"doc_id.txt", "w") as f:
        f.write(str(docID))


def clean_print():
    for word in invertedIndex:
        print(word)
        for posting in invertedIndex[word]:
            print('\t', end = "")
            print(posting)

if __name__ == "__main__":
    #file = str(sys.argv[1])
    # file = r"C:\Users\David Lee\Desktop\DEV"
    # indexBuilder(file)
    #data = json.load(file)
    #print(data['url'])
    #file.close()
    #path = "C:\Users\srb71\Documents\CS121 Test Data\ANALYST"
    createIndex()
    #clean_print()