#THINGS TO IMPORT
from __future__ import division
import nltk, requests, re, pprint, urllib, string
import sys
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
#-------------------------------------------------------------

#opening corpus file,reading and decoding
f = open('corpora_v2.XML')
raw_corpora = f.read()
raw_corpora = raw_corpora.decode('utf-8')

#total turns for entire corpus
turn_count = raw_corpora.count('</utt>')
#total number of dialogs
dialog_count= raw_corpora.count('</s>')
#average number of turns per dialog
avg_turns = turn_count / dialog_count

#finding the number of participants per dialog
raw_corpora_list = raw_corpora.split()
ParticipantsPerPost = {}
currentMax = 2
for index, word in enumerate(raw_corpora_list):
    if '<utt' in word:
        check = raw_corpora_list[index+1]
        current = int(re.search(r'\d+', check).group())
        if current > currentMax:
            currentMax = current
    if '</s>' in word:
        if ParticipantsPerPost.get(currentMax) == None:
            ParticipantsPerPost[currentMax] = 1
        else:
            ParticipantsPerPost[currentMax] = ParticipantsPerPost[currentMax] + 1
        currentMax = 2

#finding the number of comments per unique user in a single dialog
CommentsPerPost = {} #key = number of replies per user, value= number of occurrences
CurrentPostComments = {} #key = userId number, value = number of times they posted
for index, word in enumerate(raw_corpora_list):
    if '<utt' in word:
        check = raw_corpora_list[index+1]
        current = int(re.search(r'\d+', check).group())
        if CurrentPostComments.get(current) == None:
            CurrentPostComments[current] = 1
        else:
            CurrentPostComments[current] = CurrentPostComments[current] +1
    if '</s>' in word:
        for key in CurrentPostComments:
            if CommentsPerPost.get(CurrentPostComments[key]) == None:
                CommentsPerPost[CurrentPostComments[key]] = 1
            else:
                CommentsPerPost[CurrentPostComments[key]] = CommentsPerPost[CurrentPostComments[key]] +1
        CurrentPostComments = {} #clear the current post after we reach the end tag

#method to remove xml tags, anyhting inside <>
cleaned_corpora = re.sub('<.*?>', ' ', raw_corpora)

#using NLTK regextokenizer
#taking only sequences of alphanumeric characters as tokens and drops everything else
#this is one way of ignoring all punctuation
#corpora now a list of tokens/words
tokenizer = RegexpTokenizer(r'\w+')
cleaned_corpora = tokenizer.tokenize(cleaned_corpora)
#making everything lowercase
cleaned_corpora = [w.lower() for w in cleaned_corpora]

#----------STATS---------------------------------
#total number of words
total_words = len(cleaned_corpora)
#total number of distinct words
distinct_words = len(set(cleaned_corpora))
#lexical diversity, or percentage of total vocabulary that is distinct
lexical_diversity = (distinct_words / total_words)*100
#average number of words per turn
avg_wordsperturn = len(cleaned_corpora) / turn_count

#finding the french articles of text in the text and removing it
#good way to remove common words that don't really help us in look at word usage
stop_words = set(stopwords.words('french'))
#stop_words.add("les")
cleaned_corpora = [i for i in cleaned_corpora if i not in stop_words]

#Using NLTK's FreqDist method, finding top ten words used, can increase to any number
freqdist = FreqDist(cleaned_corpora)
topwords = freqdist.most_common(50)

#------------------PRINT------------------------
#print all the info
print("total # of words:")
print(total_words)
print("total # of distinct words:")
print(distinct_words)
print("ratio distinct number of words : total number of words")
print(lexical_diversity)
print("total # of turns:")
print(turn_count)
print("total # of dialogs:")
print(dialog_count)
print("average # of turns/dialog:")
print(avg_turns)
print("average # of words/turn:")
print(avg_wordsperturn)
print("Frequency of users per dialog:")
print(ParticipantsPerPost)
print("Frequency of comments made by a unique user in a dialog:")
print(CommentsPerPost)
print("top 50 words used:")
print(topwords)
