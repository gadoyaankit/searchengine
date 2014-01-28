import operator
outputfile = open("outputmodel1.txt", "w")
outputfile.close()
def run_model_4(search_output, query, bagofwords, avg_document_length, avg_query_length, document_information_dict, term_information_dict, total_terms):
    count = 0
    wordcount = 0
    document_dictonary = dict()
    ctfDict = dict()
    while wordcount < len(bagofwords):
        ctf = float(search_output[count])
        df = int(search_output[count + 1])
        ctfDict[wordcount] = ctf
        i = count + 2
        while i < count + df * 3 + 2:
            docid = int(search_output[i])
            if document_dictonary.has_key(docid):
                document_dictonary.get(docid).append([wordcount, ((0.2 * float(search_output[i + 2]) / float(search_output[i + 1])) + (0.8 * (ctf / total_terms)))])
            else:
                document_dictonary[docid] = [[wordcount, ((0.2 * float(search_output[i + 2]) / float(search_output[i + 1])) + (0.8 * (ctf / total_terms)))]]
            i = i + 3
        count = count + df * 3 + 2
        wordcount = wordcount + 1
    #calculate denominator part (square root) of query
    for docId in document_dictonary.keys():
        score = 1
        flagDict = dict() 
        for wordinfo in document_dictonary[docId]:
            score = score * wordinfo[1]
            flagDict[wordinfo[0]] = 1
        for i in ctfDict.keys():
            if not flagDict.has_key(i):
                if ctfDict[i] != 0:
                    score = score * (0.8 * ctfDict[i] / total_terms )
        document_dictonary[docId] = score #/ math.sqrt(denominator * QuerySquare)
    sorted_docDict = sorted(document_dictonary.iteritems(), key=operator.itemgetter(1), reverse=True)
    outputfile = open("outputmodel4.txt", "a")
    rank = 1
    for item in sorted_docDict[0:1000]:
        outputfile.write(str(query) + " Q0 " + "CACM-" + str(item[0]) + " " + str(rank) + " " + str(item[1]) + " Exp\n")
        rank = rank + 1
    outputfile.close()
