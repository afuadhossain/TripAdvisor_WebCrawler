# TripAdvisor_WebCrawler

This web crawler processes through french TripAdvisor forums, creating a french corpus xml file for natural language processing purposes. 

	ParseTripAdvisor.py -> the webcrawler, creates the corpus xml file

	lxmrah_fre.xml.xml  -> a sample XML that was created by ParseTripAdvisor.py

	Corpus_Analysis.py  -> analyzes the produced xml file and provides common NLP statistics

Before running Corpus_Analysis.py on the command prompt, modify line 12:

	f = open('FILENAME')

with the desired XML file to be analyzed
