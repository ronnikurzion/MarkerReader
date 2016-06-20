from ddlite import *
import PyPDF2
from Tkinter import Tk
from tkFileDialog import askopenfile

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfile().name
text = open(filename, "r").read()
# pdfReader = PyPDF2.PdfFileReader(open(filename))
# count = 1
# while count < pdfReader.numPages:
#     pageObj = pdfReader.getPage(count)
#     text = text + " " + pageObj.extractText()
#     count += 1
sentence_parser = SentenceParser()
list = sentence_parser.parse(text)
word_positions = []
count = 0
for sentence in list:
    # counternumerodos = 0
    # while counternumerodos < len(sentence.poses):
    #     print sentence.poses[counternumerodos] + "  |  " + sentence.words[counternumerodos]
    #     counternumerodos += 1
    for thing in sentence.poses:
        if thing == "NN":
            word_positions.append(count)
        count+=1

        # for wordposition in word_positions:
        #     if not len(sentence.words[wordposition]) <= 2 and sentence.dep_labels[wordposition] == "appos":
        #         print sentence.words[wordposition] + "  |  " + sentence.dep_labels[wordposition]
        # word_positions = []
        # count = 0
    count = 0
    while count < len(sentence.words):
        print(sentence.words[count] + "  |  " + sentence.dep_labels[count] + "  |  " + str(sentence.poses[count]))
        count += 1
