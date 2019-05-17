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
        doc_id_ls.append("Q" + doc_id + "_~s~_"+ str(sent_num))
    return doc_id_ls

start = time.time()
N = 0
m = 0
queries = []
##in this block I am going over all claims in training set and converting them to entitites, just first 1000
for obj in data:
    evidence_set = get_doc_id(data[obj]["evidence"])
    m+=1
    search = data[obj]["claim"]
    search = preprocess(search)
    if search and evidence_set:
        queries.append((search, evidence_set))
    if m>1000:
        break
print("done")
total  = 0
m = 0
evid = []


##I am meausirng the recall of those entities
for q in queries:
    facts = query.query_fact_normally(q[0], 500)
    evid = []
    for e in q[1]:
        evid.append(query.query_id(e))
    for e in evid:
        total +=1
        if e in facts:
            m += 1
    print(evid)
print(m, total)
