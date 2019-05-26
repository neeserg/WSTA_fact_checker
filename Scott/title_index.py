import xapian
from time import time
import os,os.path
import unicodedata
import json

DATA_FILEPATH = "/WebSearchProj/wiki-pages-text/"
DATABASE_FILEPATH = "/home/xusheng/Downloads/ano-titles"

if not os.path.exists(DATABASE_FILEPATH):
	os.mkdir(DATABASE_FILEPATH)

db = xapian.WritableDatabase(DATABASE_FILEPATH, xapian.DB_CREATE_OR_OPEN)

term_generator = xapian.TermGenerator()
term_generator.set_stemmer(xapian.Stem("en"))

total_start_time = time()

store_title = []

for i in range(1,110):
	current_file = "wiki-{:03d}.txt".format(i)

	start_time = time()
	print("currently reading file:",current_file)
	with open(DATA_FILEPATH + current_file) as file:
		previous_title = ""

		for line in file:
			line = unicodedata.normalize('NFD',line) # in case of non-english characters
			#line = (line.replace('-LRB-','(')).replace('-RRB-',')')
			line = line.split(' ')

			doc_title = line[0]


			if doc_title != previous_title:
				document = xapian.Document()
				term_generator.set_document(document)
				term_generator.index_text(doc_title.replace("_"," ").lower())
				current_data = {"title": doc_title}
				document.set_data(json.dumps(current_data))
				document.add_boolean_term(u"Q" + doc_title)
				db.replace_document(u"Q" + doc_title, document)
				previous_title = doc_title
	print("current_file" + current_file + "used time is:", time() - start_time)
print("The whole index program costs", time() - total_start_time, "seconds")
