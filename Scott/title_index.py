import xapian 
from time import time
import os,os.path
import unicodedata
import json

DATA_FILEPATH = "/mnt/wiki-pages-text/"
DATABASE_FILEPATH = "/mnt/title_based_index"

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
		previous_content = ""
		
		for line in file:
			line = unicodedata.normalize('NFD',line) # in case of non-english characters
			#line = (line.replace('-LRB-','(')).replace('-RRB-',')')
			line = unicodedata.normalize('NFD',line)
			line = line.split(' ')

			doc_title = line[0]
			sentence = ' '.join(line[1:])
			
			#previous_title = doc_title
			#previous_conten = sentence
			
			if doc_title != previous_title:
				
				document = xapian.Document()
				term_generator.set_document(document)
				term_generator.index_text(previous_content.replace("__",'-'),1,'S')
				term_generator.index_text(previous_title.replace("_"," "),1,'T')
				#term_generator.increase_termpos()
				
				current_data = {"previous_title": previous_title, "previous_content": previous_content}
				document.set_data(json.dumps(current_data))
				document.add_boolean_term(u"Q" + previous_title)
				db.replace_document(u"Q" + previous_title, document)
				
				previous_title, previous_content = "", ""
				
			previous_title = doc_title
			previous_content += sentence
			
		print("current_file" + current_file + "used time is:", time() - start_time)
				
print("The whole index program costs", time() - total_start_time, "seconds")