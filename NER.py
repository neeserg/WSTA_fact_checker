import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
import spacy

nlp = spacy.load('en_core_web_sm')

def preprocess(sent):
    sent = nlp(sent)
    query = ''
    for ent in sent.ents:
        query += ' ' + ent.text
    return query

