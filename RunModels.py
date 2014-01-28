import  porter
import m1, m2, m3, m4, m5


def get_search_output(bagofwords, term_information_dict, document_information_dict):
    search_output = []
    invindexfiles = open("inverted_index.txt").readlines()
    for word in bagofwords:
        if term_information_dict.has_key(word):
            search_output.append(int(term_information_dict[word][1]))
            search_output.append(int(term_information_dict[word][2]))
            indexline = invindexfiles[int(term_information_dict[word][3])][:-1].split()
            if indexline[0] == term_information_dict[word][0]:
                i = 1
                while i < len(indexline) - 1:
                    search_output.append(int(indexline[i]))
                    search_output.append(int(document_information_dict[indexline[i]][1]))
                    search_output.append(int(indexline[i + 1]))
                    i += 2
        else:
            search_output.append(0)
            search_output.append(0)
    return search_output

def removePunctuation(contentstring):
    for c in "!\"#$%&'()*+,./:;<=>?@[\]^_{|}~":
        contentstring = contentstring.replace(c, "")
    return contentstring

def getstopwords():
    stopwordfile = open('stop_words.txt').readlines()
    stopworddict = dict()
    commonwordcount = 0
    while commonwordcount < len(stopwordfile):
        word = stopwordfile[commonwordcount]
        commonwordcount += 1
        stopworddict[word[:-1]] = 0
    return stopworddict

# remove stop words, do stemming, return bagofwords dictionary
def parse_query(content, stopwords):
    tempbagofwords = content.replace("-", " ").split()
    bagofwords=[]
    for word in tempbagofwords:
        word = word.lower()
        if not stopwords.has_key(word):
            word = porter.stem(word)
            bagofwords.append(word)
    return bagofwords
    

def compute_avg_query_length(query_dictonary):
    avg_query_length = 0
    for querylist in query_dictonary.values():
        avg_query_length += len(querylist)
    avg_query_length = avg_query_length/len(query_dictonary.keys())
    return avg_query_length

def get_document_information():
    document_information_dict = dict()
    docinfofile = open("document_information.txt").readlines()
    for line in docinfofile:
        docline = line[:-1].split()
        # docid : unique_terms, doclength(after removing stop words)
        document_information_dict[docline[0]] = [int(docline[1]), int(docline[2])]
    return  document_information_dict 

def get_term_information():
    term_information_dict = dict()
    terminfofile = open("term_information.txt").readlines()
    for terminfo in terminfofile:
        termline = terminfo[:-1].split()
        term_information_dict[termline[0]] = termline[1:]
    return term_information_dict

def get_processed_query():
    tag_list = [".I", ".W", ".A", ".N"]
    docid = 0
    stopwords = getstopwords()
    content = ""
    querydict = dict()
    linecount = 0
    queryfile = open('query.txt').readlines()
    first_line = queryfile[linecount]
    linecount += 1
    second_line = ""
    while linecount < len(queryfile):
        second_line = queryfile[linecount]
        linecount += 1
        if first_line[0:2] == ".I":
            # process previous document
            if content != "":
                querydict[docid] = parse_query(removePunctuation(content), stopwords)
            docid = int(first_line.split()[1])
            content =""
            # save doc id
            first_line = second_line
        elif first_line[0:2] == ".W" or first_line[0:2] == ".A" or first_line[0:2] == ".N":
            while linecount < len(queryfile):
                content += second_line
                # parse title/author/text - second_line
                second_line = queryfile[linecount]
                linecount += 1
                if(second_line[0:2]) in  tag_list:
                    first_line = second_line
                    break
    content += second_line
    querydict[docid] = parse_query(removePunctuation(content), stopwords)
    return querydict


query_dictonary = get_processed_query()


corpus_information = open("Corpus_information.txt").readlines()
avg_document_length = int(corpus_information[0].split()[3])
total_terms = float(corpus_information[0].split()[1])
print total_terms
unique_terms = int(corpus_information[0].split()[0])


avg_query_length = compute_avg_query_length(query_dictonary)

document_information_dict = get_document_information()

term_information_dict = get_term_information()


# for every query run the models
for query in sorted(query_dictonary.keys()):
    search_output = get_search_output(query_dictonary[query], term_information_dict, document_information_dict)
    m1.run_model_1(search_output, query, query_dictonary[query], avg_document_length, avg_query_length, document_information_dict, term_information_dict)
    m2.run_model_2(search_output, query, query_dictonary[query], avg_document_length, avg_query_length, document_information_dict, term_information_dict)
    m3.run_model_3(search_output, query, query_dictonary[query], avg_document_length, avg_query_length, document_information_dict, term_information_dict, unique_terms) 
    m4.run_model_4(search_output, query, query_dictonary[query], avg_document_length, avg_query_length, document_information_dict, term_information_dict, total_terms)  
    m5.run_model_5(search_output, term_information_dict, query, query_dictonary[query], avg_document_length, document_information_dict)