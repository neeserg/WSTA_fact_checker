##export XAPIAN_FLUSH_THRESHHOLD=200000; python index_alldoc.py
import xapian
import time
DATA_FILEPATH = "/Users/neesergparajuli/Dropbox/Webtext/Data/wiki-pages-text/"
DATABASE_FILEPATH = "/Users/neesergparajuli/Dropbox/Webtext/Data/XxapianDatabase4"
start = time.time()
db = xapian.WritableDatabase(DATABASE_FILEPATH, xapian.DB_CREATE_OR_OPEN)

termgenerator = xapian.TermGenerator()
termgenerator.set_stemmer(xapian.Stem("en"))
text = ''
content = ''
prev_docid = ''
j = 0
first_done = False
for i in range(1,110):
    st = "wiki-{:03d}.txt".format(i)
    cyclestart = time.time()
    print(st)
    with open(DATA_FILEPATH + st) as file:
       
        #Create the databse
        for line in file:
            words = line.split(' ')
            
            #extract the title from the id

            id1 = words[0]
            docId = u"Q"+id1 + "_~s~_"
            id2 = words[1]
            if not id2.isdigit():
                continue
            
            
            if(docId != prev_docid and first_done):
                doc = xapian.Document()
                termgenerator.set_document(doc)
                #termgenerator.index_text(content)
                termgenerator.index_text(title, 1,'S')
                doc.set_data(text)
                doc.add_boolean_term(prev_docid)
                db.replace_document(prev_docid, doc)
                
                if (j%10000 == 0):
                    print(prev_docid +"--------" + text)
                    print(content)
                    print(j)
                text = ''
                content = ''
                j+=1

            ############# update document information
            title = id1.split('_')
            title = ' '.join(title)
            content += ' '.join(words[2:])
            text += '*_*' + id2 + ' '.join(words[2:])
            prev_docid = docId
            first_done = True

    print(st, time.time() - cyclestart)

print("This program took this many seconds: ",time.time() - start )
