import xapian

DATABASE_FILEPATH = "/Users/neesergparajuli/Dropbox/Webtext/Data/XxapianDatabase"

db = xapian.Database(DATABASE_FILEPATH)

queryparser = xapian.QueryParser()
queryparser.set_stemmer(xapian.Stem("en"))
queryparser.set_stemming_strategy(queryparser.STEM_SOME)

query = queryparser.parse_query("NBA finals")

enquire = xapian.Enquire(db)
enquire.set_query(query)

for match in enquire.get_mset(0, 10):
    print(match.document.get_data())