import sys
import json
from pathlib import Path
import os
import nltk
from nltk.stem.snowball import SnowballStemmer
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.tokenize import sent_tokenize, word_tokenize

#INVERSE INDEX
# TODO: keep track of when to write to disc
# TODO: merging and writing to disc
# TODO: how to organize inverted index for better merging
# TODO: what data structure for inverse index

#QUERY FUNCTIONS
# TODO: Query searching
# TODO: tf-idf function


class inverseIndex():

    def __init__(self, directory):
        self.docCounter = 0
        self.fileCounter = 0
        self.directory = directory

        # use this to write to disc. every 33% we write to disc
        self.fileTotal3 = self.fileTotalFcn(self.directory)
        self.fileTotal2 = int(2 * self.fileTotal3/3)
        self.fileTotal1 = int(self.fileTotal3/3)

    # gets the total number of files in the directory
    def fileTotalFcn(self, directory):
        asdf = Path(directory).rglob("*.json")
        counter = 0
        for i in asdf:
            counter += 1

        return counter

    # gets all the folders
    def indexFiles(self):
        for folders in os.listdir(self.directory):
            # folder = iterator of folders?
            folder = os.path.join(self.directory, folders)
            # one folder is passed into the function
            self.processFolders(folder)


    #gets all the files in one folder
    def processFolders(self, folder):
        for filename in os.listdir(folder):
            filePath = os.path.join(folder, filename)
            self.indexBuilder(filePath)
            self.docCounter += 1
            self.fileCounter += 1

    def indexBuilder(self, file):
        # our stemmer method
        snow_stemmer = SnowballStemmer(language='english')

        # where to store our inverted index
        # TODO: need to clear after every write to disc
        I = defaultdict(list)


        f = open(file)
        data = json.load(f)


        # tokenization
        htmlText = data['content']
        tokenized = BeautifulSoup(htmlText, "html.parser")

        # stemmer
        completeToken = set(snow_stemmer.stem(tokenized))

        # dictionary structure
        # {"token":[list]}

        #list structure
        #list[0] is the frequency
        #list[1:] is the docs
        #example
        # [4, 0, 7, 62, 88]

        for token in completeToken:
            if token not in I.keys():
                I[token] = [0]
            I[token].append(self.docCounter)
            I[token][0] += 1


        # write to file conditional
        if self.fileCounter == int(self.fileTotal1):
            return
            # write to file
            #clear dictionary
            #merge option 1

        if self.fileCounter == int(self.fileTotal2):
            return
            #write to file
            #clear dictionary
            #merge option 1

        if self.fileCounter == int(self.fileTotal3):
            return
            #write to file
            #clear dictionary
            # merge option 1
        #call merge function option2


#asdfasdfasdf









if __name__ == "__main__":
    #file = str(sys.argv[1])
    # file = r"C:\Users\David Lee\Desktop\DEV"
    # indexBuilder(file)
    #data = json.load(file)
    #print(data['url'])
    #file.close()

    tester = inverseIndex(r"C:\Users\David Lee\Desktop\DEV")