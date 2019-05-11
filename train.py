import json
import query
import time
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
for obj in data:
    m +=1
    search = data[obj]["claim"]
    facts = query.query_fact_normally(search, 10)
    # for doc in get_doc_id(data[obj]["evidence"]):
    #     evid = query.query_id(doc)
    print(m, facts, time.time() - start)

