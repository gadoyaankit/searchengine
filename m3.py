import operator
outputfile = open("outputmodel3.txt", "w")
outputfile.close()
def run_model_3(search_output, query, bagofwords, avg_document_length, avg_query_length, document_information_dict, term_information_dict, unique_terms):
    count = 0
    wordcount = 0
    document_dictonary = dict()
    while wordcount < len(bagofwords):
        df = int(search_output[count + 1])
        i = count + 2
        while i < count + df * 3 + 2:
            docid = int(search_output[i])
            if document_dictonary.has_key(docid):
                document_dictonary.get(docid).append([wordcount, float(search_output[i + 1]), (float(search_output[i + 2]) + 1)/(float(search_output[i + 1]) + unique_terms)])
            else:
                document_dictonary[docid] = [[wordcount, float(search_output[i + 1]), (float(search_output[i + 2]) + 1)/(float(search_output[i + 1]) + unique_terms)]]
            i = i + 3
        count = count + df * 3 + 2
        wordcount = wordcount + 1    
    #calculate denominator part (square root) of query
    for docId in document_dictonary.keys():
        score = 1
        for wordinfo in document_dictonary[docId]:
            score = score * wordinfo[2]
        for i in range(len(document_dictonary[docId]), len(bagofwords)):
            score = score * (1/(document_dictonary[docId][0][1] + unique_terms))
        document_dictonary[docId] = score #/ math.sqrt(denominator * QuerySquare)
    sorted_docDict = sorted(document_dictonary.iteritems(), key=operator.itemgetter(1), reverse=True)
    outputfile = open("outputmodel3.txt", "a")
    rank = 1
    for item in sorted_docDict[0:1000]:
        outputfile.write(str(query) + " Q0 " + "CACM-" + str(item[0]) + " " + str(rank) + " " + str(item[1]) + " Exp\n")
        rank = rank + 1
    outputfile.close()

