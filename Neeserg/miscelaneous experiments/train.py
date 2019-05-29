import json
import query
import time
from NER import preprocess
##load the evidence
TRAINING_SET = "/Users/neesergparajuli/Dropbox/Webtext/Data/train.json"

data = {}
with open(TRAINING_SET) as file:
    data = json.load(file)

##get all the doc ids
def get_doc_id(evidence_list):
    doc_id_ls = []
    for evidence in evidence_list:
        doc_id = evidence[0]
        sent_num = evidence[1]
        idd = "Q" + doc_id #+ "_~s~_"+ str(sent_num)
        doc_id_ls.append(idd)
    return doc_id_ls

start = time.time()
N = 0
m = 0
queries = []
##in this block I am going over all claims in training set and converting them to entitites, just first 1000
searches_ = {}
for obj in data:
    evidence_set = get_doc_id(data[obj]["evidence"])
    m+=1
    search = data[obj]["claim"]
    search = preprocess(search)
    searches_["-".join(search)] = data[obj]["claim"]
    if search and evidence_set:
        queries.append((search, evidence_set))
    if m>1000:
        break
print("done")
total  = 0
m = 0
evid = []


##I am meausirng the recall of those entities
from collections import Counter
count = Counter()
for q in queries:
    facts = query.query_fact_normally(q[0], 5)
    # print(facts)
    evid = []
    for e in q[1]:
        evid.append(query.query_id(e))
    n = 0
    tt = 0
    for e in evid:
        tt = 1
        if e in facts:
            c = facts.index(e)
            count[c+1]+=1
            n = 1
        # else:
        #     print(q[0])
        #     print(searches_['-'.join(q[0])])
        #     print(facts)
        #     print(e) 
    m+=n
    total+=tt
print(m, total)
count[0] = 0
print(count)