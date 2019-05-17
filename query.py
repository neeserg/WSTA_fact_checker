import xapian
import time 

DATABASE_FILEPATH = "/Users/neesergparajuli/Dropbox/Webtext/Data/XxapianDatabase"

db = xapian.Database(DATABASE_FILEPATH)

def my_own_queryparser(fact):
    print(fact)
    fact = fact.split()
    new_fact = ''
    for f in fact:
        if f.isalpha() or f.isalnum():
            new_fact += 'title:' +f + ' ' ## 'text:' + f.lower() + 
    return new_fact

def query_fact_normally(fact, k_matches):
    # initiate stemmer for query

    queryparser = xapian.QueryParser()
    queryparser.add_prefix("text", "Z")
    queryparser.add_prefix("title", "S")
    query = queryparser.parse_query(my_own_queryparser(fact))
    print(query)
    enquire = xapian.Enquire(db)
    enquire.set_query(query)

    return set(match.document.get_docid() for match in enquire.get_mset(0,k_matches))

def query_id(abool_term):
    bool_term =  xapian.Query(abool_term)
    enquire = xapian.Enquire(db)
    enquire.set_query(bool_term)
    matches = [match.document.get_docid() for match in enquire.get_mset(0,8)]
    if len(matches)>1:
        print(matches)
    if len(matches) ==0:
        print(abool_term + "doesnt exist")
        return None
    sentence = matches[0]
    return sentence

# print(query_id("QRoman_Atwood_~s~_1"))

# print(query_fact_normally("Roman Atwood is a content creator", 8))