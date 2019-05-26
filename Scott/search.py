#! -*- coding=utf-8 -*-
'''
Given a claim return the match documents for it
'''
import xapian
import sys
import json
from collections import defaultdict
from collections import Counter
from nltk.corpus import stopwords
from  nltk.tokenize import word_tokenize
import spacy
import en_core_web_sm
import datetime
import string
import unicodedata




nlp = en_core_web_sm.load() #load for spacy to do NER

def ner(sent):
    doc = nlp(sent)
    query = ""
    for entity in doc.ents:
        query += entity.text
    return query

def noun_phrases(sent):
    doc = nlp(sent)
    noun_phrase = [chunk.text for chunk in doc.noun_chunks]
    ner_text = [entity.text for entity in doc.ents]
    result = []
    for x in noun_phrase:
        if x not in ner_text:
            ner_text.append(x)
    return " ".join(ner_text)

def noun(sent):
    doc = nlp(sent)
    return " ".join([chunk.text for chunk in doc.noun_chunks])

def search_query(claim):
    stopWords=set(stopwords.words('english'))
    claim = word_tokenize(claim)
    claim = " ".join([w for w in claim if w not in stopWords])
    #print(claim)
    claim = noun_phrases(claim)
    #print(claim)
    db=xapian.Database('/home/xusheng/Downloads/ano-titles')
    query_parser=xapian.QueryParser()
    query_parser.set_stemmer(xapian.Stem('en'))
    query_parser.set_stemming_strategy(query_parser.STEM_SOME)
    #query = query_parser.parse_query("title:"+claim)
    query =query_parser.parse_query(claim)

    enquire=xapian.Enquire(db)
    enquire.set_query(query)
    matches=[]

    for match in enquire.get_mset(0,5):
        match_doc=json.loads(match.document.get_data().decode('utf8')) #the match data is parse as python dict.
        doc_title=match_doc.get('title')

        matches.append(match_doc)

    return matches

if __name__=='__main__':
    FILE_PATH = "/home/xusheng/Downloads/devset.json"
    with open(FILE_PATH) as f:
        data_file = json.load(f)
    m = 0
    claim_evid_pair = []

    for obj in data_file:
        if data_file[obj]["evidence"] != []:
            evidence_list = []
            for i in data_file[obj]["evidence"]:
                if i[0] not in evidence_list:
                    evidence_list.append(i[0])
            claim_evid_pair.append((data_file[obj]["claim"],evidence_list))


    temp = length = 0
    temp_recall = 0
    search_terms = 0
    for item in claim_evid_pair:
        #claim_result = search_query(item[0])
        claim_result = search_query(item[0])
        search_terms += len(claim_result)
       # a = str([item[0],claim_result])
       # f.write(a)
        #claim_result = search_query(noun_phrases(item[0]))
        if m < 10:
            print(item[0])
            print(noun_phrases(item[0]))
            print(ner(item[0]))
        #claim_result = search_query(ner(item[0]))
        true = 0

        for i in claim_result:
            if i["title"] in item[1]:
                #if j in i["sentences"]:
                true += 1

        temp_recall += true / len(item[1])#calculate the current "recall" for this claim
        temp += true
        length += len(item[1])
       # print(true, len(item[1]))[chunk.text for chunk in doc.noun_chunks]
        m += 1
        #if m >= 1000:
           # break

    recall = temp_recall / m #average recall
    precision = temp / search_terms
    print("precision:",precision)
    print("The recall is:", recall)
    print("F1 Score:",2*recall*precision/(precision+recall) )
    print(temp, length)

