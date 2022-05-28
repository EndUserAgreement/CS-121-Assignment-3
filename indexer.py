import re
import json
import lxml
import os
import math
import pprint
from nltk.stem.snowball import SnowballStemmer#
from bs4 import BeautifulSoup#
from nltk.tokenize import word_tokenize

#from simhash import Simhash, SimhashIndex   CHECK THIS

#LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", ""]
LETTERS = ["g", ""]
#letterhold = defaultdict(letters)
docID=[]
invertedIndex = {}
#hashed = SimhashIndex([], k=1)
stemmer = SnowballStemmer(language="english")
indexpath = r"C:\Users\srb71\Documents\GitHub\CS-121-Assignment-3\indexes"
datapath = r"C:\Users\srb71\Documents\CS121 Test Data\MYTEST"

""" 
class Posting:
    def __init__(self, docid, tfidf, fields):
        self.docid = docid
        self.tfidf = tfidf # use freq counts for now
        self.fields = fields
"""
 

#parse through the json file and extract all words, return whole doc as one large string
def parse_json(path):
    with open(path, "r", encoding="utf-8") as read_file: # CHANGED ENCODING, CAN REMOVE LATER
        #read_file.decode('utf-8-sig')
        file = json.load(read_file)
    soup = BeautifulSoup(file["content"], "lxml")
    for word in soup.find_all(['script', 'style']):
        word.extract()
    content = soup.get_text(" ")
        #print(content)
    for letter in content:
        if bool(re.match(r'[^\x20-\x7F]+',letter)) == True:
            content.replace(letter,"")
    headers = soup.find_all(['h1', 'h2', 'h3', 'b', 'a'], text=True)
    headers = ' '.join([t.string for t in headers])
    for word in headers:
            #print(headers)
        for letter in word:
            if bool(re.match(r'[^\x20-\x7F]+',letter)) == True:
                word.replace(letter,"")
    return content + " " + headers


 #Returns a list of tf-ids for each word in document
def process_tfid(document: str):
    document = word_tokenize(document.lower().replace('\\',''))
    stemmed = [stemmer.stem(word) for word in document]
    tfids = {}
    for word in stemmed:
        for letter in word:
            if bool(re.match(r'[^\x20-\x7F]+',letter)) == True:
                word.replace(letter,"")
        if word in tfids: 
            tfids[word] += 1
        else: 
            tfids[word] = 1
    for word in tfids:
        tfids[word] = round(math.log(tfids[word]) + 1, 4)
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
        combine(tf_dict, current_doc) #was indented
    os.chdir('..') #leave the current directory

#starts the processing of the DEV file
def process():
    os.chdir(datapath)
    index_count = 1
    for f in os.listdir(os.getcwd()):
        if os.path.isdir(f):
            processFolder(f)
        if len(invertedIndex) > 100:
            writeToFile(index_count)
            index_count += 1
    if len(invertedIndex) > 0:
        writeToFile(index_count)

def writeToFile(count: int):
    with open(indexpath + "\index" + str(count) + ".txt", "w", encoding="utf-8") as file:
        file.write(str(invertedIndex))
    #clean_print()
    invertedIndex.clear()


def createIndex():
    #index_count = 1
    #DELETION
    #while(os.path.exists("indexes/partial_index"))
    process()
    os.chdir("..")

    with open(indexpath + "\doc_id.txt", "w", encoding="utf-8") as f:
        f.write(str(docID))


def clean_print():
    for word in invertedIndex:
        print(word)
        for posting in invertedIndex[word]:
            print('\t', end = "")
            print(posting)


def merge():
    index_list = getIndexes() #change name
    #start the splitting up of the index by letter, store the letter:line number in a seperate file
    for letter in LETTERS:
        print(letter)
        lettersdict = makefull(letter, index_list)
        with open(indexpath + "\index" + letter + ".txt", "w", encoding="utf-8") as opfile:
            wordline = 1
            for word in lettersdict:
                if word.endswith("\\"):
                    print("{\"" + word + "\\" + "\": " + str(lettersdict[word]) + "}", file=opfile)
                else:
                    print("{\"" + word + "\": " + str(lettersdict[word]) + "}", file=opfile)
                with open(indexpath + "\word_number.txt", "a", encoding="utf-8") as wordnum:
                    if word.endswith("\\"):
                        print(word + "\\" + " " + str(wordline), file=wordnum)
                    else:
                        try:
                            print(word + " " + str(wordline), file=wordnum)
                        except:
                            print("")
                wordline +=1

def makefull(letter:str, indexlist:list):
    index = {}
    for entry in indexlist:
        print(entry)
        temp = makepartial(letter, entry)
        index.update(temp)
        #print(index)
    return index
    
def makepartial(letter:str, partialindex:str):
    partindex = {}
    with open(partialindex, "r", encoding="utf-8") as file:
        tempindex = eval(file.read())
    #print(tempindex)
    #print(tempindex.keys())
    if letter != "": #adds all keys that start with letter to a temp index, then returns it
        for word in [key for key in tempindex.keys() if key.startswith(letter)]:
            partindex[word] = tempindex[word]
            print(word)
    else: # if its a number
        for word in [key for key in tempindex.keys() if key[:1] not in LETTERS]:
            partindex[word] = tempindex[word]
    return partindex


def getIndexes():
    index = []
    indexCount = 1
    while(os.path.exists(r"C:\Users\srb71\Documents\GitHub\CS-121-Assignment-3\indexes\index" + str(indexCount) + ".txt")):
        index.append(r"C:\Users\srb71\Documents\GitHub\CS-121-Assignment-3\indexes\index" + str(indexCount) + ".txt")
        indexCount += 1
    print(index)
    return index

if __name__ == "__main__":
    #path = "C:\Users\srb71\Documents\CS121 Test Data\ANALYST"
    createIndex()
    merge()
    #clean_print()