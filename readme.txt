Technology used for coding:
Python 2.7

How to run the program:
Run cacm_parser.py. It may take few seconds to run the program as it creates Inverted index.
After the parser has finish executing, it will output following files:
	--term_information.txt
	--corpus_information.txt
	--document_nformation.txt
	--inverted_index.txt

Once this is done, run the file run_models.py.
This will execute all the five models.
The program will output 5 output files. Each file corresponds to one of the models.

	--outputmodel1.txt  --> Okapi-tf
	--outputmodel2.txt  --> Okapi-tf times idf	
	--outputmodel3.txt  --> Language modeling - Laplace
	--outputmodel4.txt  --> Language modeling - Jelinik-Mercer
	--outputmodel5.txt  --> BM25

To run the perl script use the following command:
perl trec_eval.pl cacm.rel outputmodel#.txt

where # = {1,2,3,4,5}


