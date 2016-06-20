from ddlite import *

markerDatabase = []
diseaseDatabase = []
filename = "AGR2_blood_biomarker.txt"

print "OPENING FILE: " + filename
text = open(filename, "r").read()
sentence_parser = SentenceParser()
list = sentence_parser.parse(text)
words = []

for sentence in list:
    i = 0
    while i < len(sentence.words):
        word = sentence.words[i]
        if (sentence.dep_labels[i] == "compound"):
            while (sentence.dep_labels[i] == "compound"):
                i += 1
                word += " " + sentence.words[i]
        words.append(word.lower())
        i += 1
