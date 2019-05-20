import xapian
import json
import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from xapian import BoolWeight

nlp = spacy.load('en_core_web_sm')

def ner(sent):
    sent = nlp(sent)
    query = ""
    for entity in sent.ents:
        query += " " + entity.text
    return query

def search_query(querystring):
        DATAFILE_PATH = "/mnt/title_based_index"
        dbpath = DATAFILE_PATH
        db = xapian.Database(dbpath)

        queryparser = xapian.QueryParser()
        queryparser.set_stemmer(xapian.Stem("en"))
        queryparser.set_stemming_strategy(queryparser.STEM_SOME)
        queryparser.add_prefix("title",'T')
        queryparser.add_prefix("sentence","S")

        query = queryparser.parse_query(querystring)
        enquire = xapian.Enquire(db)
        ##BM25
        #TFIDF enquire.set_weighting_scheme(TfIdfWeight())
        enquire.set_weighting_scheme(BoolWeight())
        enquire.set_query(query)

        matches = []
        match_titles = []
        match_sentences = []
        for match in enquire.get_mset(0, 100):
                fields = json.loads(match.document.get_data().decode('utf-8'))
                match_titles.append(fields.get('previous_title'))
                match_sentences.append(fields.get('previous_content'))
                matches.append((match.rank, match.docid))

        print(match_titles)
        return  match_titles

if __name__ == '__main__':
    FILE_PATH = "devest.json"
    with open(FILE_PATH) as f:
        data_file = json.load(f)
    m = 0
    evidence_set = []

    for obj in data_file:
        evidence = data_file[obj]["evidence"]
        temp = [n[0] for n in evidence]
        for term in temp:
            if term not in evidence_set:
                evidence_set.append(term)
        search = ner(data_file[obj]["claim"])

    true_pos  = []
    search_result = search_query("title:The Mod Squad is an American movie.")
    true = 0
    for item in search_result:
        print(item)
        m += 1
        if m > 10:
            break
        if item in evidence_set:
            true += 1
            true_pos.append(item)
    recall = true / len(evidence_set)
    print("true is:", true)
    print("The recall is:", recall)
    print(true_pos)
    print(evidence_set)
