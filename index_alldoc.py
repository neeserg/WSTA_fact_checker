
import xapian
import time
DATA_FILEPATH = "/Users/neesergparajuli/Dropbox/Webtext/Data/wiki-pages-text/"
DATABASE_FILEPATH = "/Users/neesergparajuli/Dropbox/Webtext/Data/XxapianDatabase"
start = time.time()
db = xapian.WritableDatabase(DATABASE_FILEPATH, xapian.DB_CREATE_OR_OPEN)

termgenerator = xapian.TermGenerator()
termgenerator.set_stemmer(xapian.Stem("en"))

for i in range(1,110):
    st = "wiki-{:03d}.txt".format(i)
    cyclestart = time.time()
    print(st)
    j = 0
    with open(DATA_FILEPATH + st) as file:
       
        #Create the databse
        for line in file:
            words = line.split(' ')
            
            #extract the title from the id

            id1 = words[0]
            title = id1.split('_')
            title = ' '.join(title)
            title = title.split('-')
            title = ' '.join(title)

            #check fact number is given and create doc ID
            id2 = words[1]
            if not id2.isdigit():
                continue
            docId = u"Q"+id1 + "_~s~_"+id2

            #create main fact refference
            text = ' '.join(words[2:])
            doc = xapian.Document()
            termgenerator.set_document(doc)
            termgenerator.index_text(text)
            termgenerator.index_text(title, 1,'S')
            if (j%10000 == 0):
                print(docId, text)

            doc.set_data(text)
            doc.add_boolean_term(docId)
            db.replace_document(docId, doc)
            j+=1
    print(st, time.time() - cyclestart)

print("This program took this many seconds: ",time.time() - start )





        