import porter, shutil, os

# create word dictionary, store ctf, df in it.

word_dict = dict()
count = 1
number_of_documents = 0

# after removing stop words
number_of_terms = 0 

# stop word in dict format
stop_words = open('stop_words.txt').readlines()
stop_words_dict = dict()
stop_words_count = 0
while stop_words_count < len(stop_words):
    word = stop_words[stop_words_count]
    stop_words_count += 1
    stop_words_dict[word[:-1]] = 0

# removes punctuation from the content  
def remove_punctuations(content_string):
    for c in "!\"#$%&'()*+,./:;<=>?@[\]^_{|}~":
        content_string = content_string.replace(c, "")
    return content_string

# remove stop words, do stemming, return bag_of_words_dict dictionary
def parse_document_content(content, stopwords):
    tempbagofwords = content.replace("-", " ").split()
    bag_of_words_dict=dict()
    global number_of_terms
    for word in tempbagofwords:
        word = word.lower()
        if word not in stopwords:
            number_of_terms += 1
            word = porter.stem(word)
            if bag_of_words_dict.has_key(word):
                bag_of_words_dict[word] += 1
            else:
                bag_of_words_dict[word] = 1
    return bag_of_words_dict
    

# returns number unique words from bag_of_words_dict

# update document info into Docinfo file 
def update_document_information(docid, wordcount, bag_of_words_dict):
    docinfofile = open("document_information.txt", "a")
    docinfofile.write(str(docid) + " " + str(len(bag_of_words_dict.keys())) + " " + str(wordcount) + "\n")
    docinfofile.close()


def update_term_information(docid, bag_of_words_dict):
    global count
    global word_dict
    for word in bag_of_words_dict.keys():
        if(word_dict.has_key(word)):
            # term id,    ctf   df
            word_dict[word] = [word_dict[word][0] , word_dict[word][1] + bag_of_words_dict[word], word_dict[word][2] + 1]
        else: 
            word_dict[word] = [count, bag_of_words_dict[word], 1]
            count += 1
        wordfile = open("terms/" + str(word_dict[word][0]) + ".txt", "a+")
        wordfile.write(str(docid) + " " + str(bag_of_words_dict[word]) + "\n")
        
def document_processing(docid, stopwords, content):
    global number_of_documents
    number_of_documents += 1
    #print content
    bag_of_words_dict = parse_document_content(remove_punctuations(content), stopwords)
    wordcount= len(bag_of_words_dict)
    update_document_information(docid, wordcount, bag_of_words_dict)
    update_term_information(docid, bag_of_words_dict)
    
  
    
def create_inverted_index():
    global count
    global word_dict
    print "came to make inverted index"
    terminfofile = open("term_information.txt", "w")
    invindexfile = open("inverted_index.txt", "w")
    offsetcount = 0
    for word in word_dict.keys(): 
        terminfofile.write(word + " " + str(word_dict[word][0]) + " " + str(word_dict[word][1]) + " " + str(word_dict[word][2]) + " " + str(offsetcount) + "\n")
        offsetcount += 1
        # create string to add in inverted index file
        wordfile = open("terms/" + str(word_dict[word][0]) + ".txt", "r").readlines()
        wordfilecount = 0
        wordinfo = str(word_dict[word][0])
        while wordfilecount < len(wordfile):
            line = wordfile[wordfilecount]
            wordfilecount += 1
            wordinfo += " " + line[:-1]
        wordinfo += "\n"
        invindexfile.write(wordinfo)    
            
def createCorpusInfoFile():
    global number_of_terms
    global number_of_documents
    global count
    corpusinfofile = open("corpus_information.txt", "w")
    # no of unique terms, no of terms, total no of docs, avg doc length
    corpusinfofile.write(str(count) + " " + str(number_of_terms) + " " + str(number_of_documents) + " " + str(number_of_terms/number_of_documents) + "\n")
    #print count, number_of_terms, number_of_documents, str(number_of_terms/number_of_documents)
def cacm_parser():
    tag_list = [".I", ".T", ".B", ".A", ".N", ".X", ".K", ".C", ".W"]
    docid = 0
    stopwords = stop_words_dict
    content = ""
    os.mkdir("terms")
    #initialSetup()
    # empty docinfo file
    docinfofile = open("document_information.txt", "w")
    docinfofile.close()
    linecount = 0
    cacm_file = open('cacm.txt').readlines()
    first_line = cacm_file[linecount]
    linecount += 1
    while linecount < len(cacm_file):
        second_line = cacm_file[linecount]
        linecount += 1
        if first_line[0:2] == ".I":
            # process previous document
            if content != "":
                document_processing(docid, stopwords, content)
            docid = int(first_line.split()[1])
            content =""
            # save doc id
            first_line = second_line
        elif first_line[0:2] == ".T" or first_line[0:2] == ".A" or first_line[0:2] == ".W" or first_line[0:2] == ".K":
            while linecount < len(cacm_file):
                content += second_line
                # parse title/author/text - second_line
                second_line = cacm_file[linecount]
                linecount += 1
                if (second_line[0:2]) in tag_list:
                    first_line = second_line
                    break
        elif first_line[0:2] == ".B" or first_line[0:2] == ".X" or first_line[0:2] == ".N" or first_line[0:2] == ".C":
            while linecount < len(cacm_file):
                # parse  - second_line
                second_line = cacm_file[linecount]
                linecount += 1
                if (second_line[0:2]) in tag_list:
                    first_line = second_line
                    break
    document_processing(docid, stopwords, content)


cacm_parser()
create_inverted_index()
createCorpusInfoFile()
shutil.rmtree("terms")
print "End"   