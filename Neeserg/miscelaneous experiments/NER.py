import nltk
from nltk.stem import *
import spacy
nlp = spacy.load('en_core_web_sm')
##extracting named entities
def preprocess(sent):
    sent = nlp(sent)
    query = []
    for ent in sent.noun_chunks:
        if ent.root.dep_ == "nsubj":
            query.append("title:" + '"' + ent.text + '"')
    for ent in sent.ents:
        query.append("text:" + '"' + ent.text + '"')
    for token in sent:
        if token.tag_ == "NN" :
            query.append("text:" + token.text)
        elif token.pos_ == "PROPN":
            query.append("text:" + token.text)
            
    return query

# def similar(fact, )