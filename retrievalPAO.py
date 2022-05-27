from collections import defaultdict
import sys
import json
from nltk.corpus import stopwords
import requests


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

if __name__ == "__main__":

    # Get index
    index_file = "C:/Users/srb71/Documents/GitHub/CS-121-Assignment-3/urls.json"
    with open(index_file, "r") as json_file:
        index = json.load(json_file)

    # Get urls
    with open("urls.json", "r") as url_json_file:
        urls = json.load(url_json_file)

    search_words = list()

    for search_word in sys.argv[1:]:
        if search_word not in set(stopwords.words("english")):
            search_words.append(search_word)

  
    doc_ids = merge_multiple(index, *search_words)
    postings = map(lambda word: index[word], search_words)
    top_doc_ids = get_top_doc_ids(postings, doc_ids)
    top_urls = get_top_urls(top_doc_ids, urls)
    
    print("Top 5 URLS:")
    for url_info in top_urls:
        print(url_info[0])
    

    