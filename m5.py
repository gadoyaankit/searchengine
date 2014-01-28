import math, operator

outputfile = open("outputmodel1.txt", "w")
outputfile.close()
def run_model_5(search_output, term_information_dict, query, bagofwords, avg_document_length, document_information_dict):
    count = 0
    wordcount = 0
    document_dictonary = dict()
    k1 = 1.2
    b = 0.75
    while wordcount < len(bagofwords):
        df = int(search_output[count + 1])
        i = count + 2
        while i < count + df * 3 + 2:
            docid = int(search_output[i])
            tf = float(search_output[i + 2])
            firstTerm = math.log(1.0 / ((float(df) + 0.5)/(84678.0 - float(df) + 0.5)))
            K = k1 * ((1.0 - b) + b * ((float(search_output[i + 1]))/avg_document_length))
            secondTerm = ((k1 + 1.0) * tf)/(K + tf)
            bm25= firstTerm * secondTerm
            if document_dictonary.has_key(docid):
                document_dictonary.get(docid).append([wordcount, bm25])
            else:
                document_dictonary[docid] = [[wordcount, bm25]]
            i = i + 3
        count = count + df * 3 + 2
        wordcount = wordcount + 1    
    #calculate denominator part (sqaure root) of query
    for docId in document_dictonary.keys():
        score = 0
        for wordinfo in document_dictonary[docId]:
            score = score + wordinfo[1]
        document_dictonary[docId] = score #/ math.sqrt(denominator * QuerySquare)
    sorted_docDict = sorted(document_dictonary.iteritems(), key=operator.itemgetter(1), reverse=True)
    outputfile = open("outputModel5.txt", "a")
    rank = 1
    for item in sorted_docDict[0:1000]:
        outputfile.write(str(query) + " Q0 " + "CACM-" + str(item[0])  + " " + str(rank) + " " + str(item[1]) + " Exp\n")
        rank = rank + 1
    outputfile.close()
