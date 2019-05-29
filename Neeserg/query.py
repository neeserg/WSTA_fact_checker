import xapian
import time 


DATABASE = "/home/neeserg/Dropbox/Webtext/Data/XxapianDatabase"
db = xapian.Database(DATABASE)

def get_unique_id(terms):
    for term in terms:
        if "_~s~_" in term:
            ID = term.split("_~s~_" )
            sentenceId  = int(ID[1])
            docId = ID[0][1:]
            return (docId, sentenceId)
    
    print("wtdf")
    return ("wtf",1)


def my_own_queryparser(fact):
    new_fact = ''
    for f in fact:
        new_fact += f + ' ' ## 'text:' + f.lower() + 
    return new_fact

    # initiate stemmer for query
def query_fact_normally(fact, k_matches):
   
    queryparser = xapian.QueryParser()
    queryparser.set_stemmer(xapian.Stem("en"))
    queryparser.add_prefix("text", "")
    queryparser.add_prefix("title", "S")
    query = queryparser.parse_query(my_own_queryparser(fact))
    enquire = xapian.Enquire(db)
    # enquire.set_weighting_scheme(xapian.TfIdfWeight())
    enquire.set_query(query)
    return list(match.document.get_data().decode("utf8") for match in enquire.get_mset(0,k_matches))

def query_id(abool_term):
    enquire = xapian.Enquire(db)
    bool_term =  xapian.Query(abool_term)
    enquire.set_query(bool_term)
    matches = [match.document.get_data().decode("utf8") for match in enquire.get_mset(0,8)]
    if len(matches)>1:
        print(matches)
    if len(matches) ==0:
        print(abool_term + "doesnt exist")
        return None
    sentence = matches[0]
    return sentence
def get_docs(fact, k_matches):
   
    queryparser = xapian.QueryParser()
    queryparser.set_stemmer(xapian.Stem("en"))
    queryparser.add_prefix("text", "")
    queryparser.add_prefix("title", "S")
    query = queryparser.parse_query(my_own_queryparser(fact))
    enquire = xapian.Enquire(db)
    # enquire.set_weighting_scheme(xapian.TfIdfWeight())
    enquire.set_query(query)
    results = []
    for match in enquire.get_mset(0,k_matches):
        terms = match.document.termlist()
        unid = get_unique_id([term.term.decode("utf8") for term in terms])
        results.append((unid, match.document.get_data().decode("utf8")))
    return results
 

# print(query_id("QRoman_Atwood_~s~_1"))

