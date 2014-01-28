import operator
outputfile = open("outputmodel1.txt", "w")
outputfile.close()
def run_model_1(search_output, query, bagofwords, avg_document_length, avg_query_length, document_information_dict, term_information_dict):
    QueryOkapi = getQueryOkapiDetails(bagofwords, avg_document_length, avg_query_length)
    count = 0
    wordcount = 0
    document_dictonary = dict()
    while wordcount < len(bagofwords):
        df = int(search_output[count + 1])
        i = count + 2
        while i < count + df * 3 + 2:
            docid = int(search_output[i])
            if document_dictonary.has_key(docid):
                document_dictonary.get(docid).append([wordcount, (search_output[i + 2]/(search_output[i + 2] + 0.5 + (1.5 * search_output[i + 1] / avg_document_length)))])
            else:
                document_dictonary[docid] = [[wordcount, (search_output[i + 2]/(search_output[i + 2] + 0.5 + (1.5 * search_output[i + 1] / avg_document_length)))]]
            i = i + 3
        count = count + df * 3 + 2
        wordcount = wordcount + 1    
    
    for docId in document_dictonary.keys():
        score = 0
        for wordinfo in document_dictonary[docId]:
            score = score + QueryOkapi[wordinfo[0]] * wordinfo[1]
        document_dictonary[docId] = score
        
    sorted_docDict = sorted(document_dictonary.iteritems(), key= operator.itemgetter(1), reverse=True)
    outputfile = open("outputModel1.txt", "a")
    rank = 1
    for item in sorted_docDict[0:1000]:
        outputfile.write(str(query) + " Q0 " + "CACM-" + str(item[0]) + " " + str(rank) + " " + str(item[1]) + " Exp\n")
        rank = rank + 1
    outputfile.close()     
    
def getQueryOkapiDetails(bagOfWords, avg_document_length, avg_query_length):
    sd = 1/(1 + 0.5 + (1.5 * len(bagOfWords)/avg_query_length))
    QueryOkapi = [sd]*len(bagOfWords)
    return QueryOkapi 