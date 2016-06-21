

from ddlite import *

import pickle

#TODO:

#-Remove Author's names

#-Using both Dictionary Match and Syntax Match will overcount

#Parse AGR2 document into seperate Sentences

def parseDocIntoWords():

    filename = "AGR2_blood_biomarker.txt"

    text = open(filename, "r").read()

    print "OPENING FILE"

    sentence_parser = SentenceParser()

    list = sentence_parser.parse(text, 1)

    print "PARSED TEXT"

    words = []

    print "GETTING ALL WORDS"

    poses = []

    for sentence in list:

        words.append(sentence)

    print words

    return words

#BiomarkerGenerator-----------------------------------------------------------------------------------------------------

def biomarkerGenerator(words):

    #markerDatabase = ['AGR2', 'PSA', 'CGA']

    markerDatabase = []

    diseaseDatabase = ["crpc", "prostate cancer", "prostate cancer cells", "ne-crpc", "metastatic",

                       "metastatic prostate cancer", "crpc-ne"]

    with open('markerData.pickle', 'rb') as f:

        markerDatabase = pickle.load(f)

    print markerDatabase

    #Database filter:

    gene_dm = DictionaryMatch(label='MarkerName', dictionary=markerDatabase, ignore_case=False)

    #Name(Syntax) filter:

    #up_regex = RegexNgramMatch(label='Upper', regex_pattern=r'(^|(?<=\s))[A-Za-z][A-Z1-6-]{2,}', ignore_case=False,match_attrib='words')

    #word_regex = RegexFilterAll(up_regex, label='Word', regex_pattern=r'[A-Za-z]{2,}', ignore_case=True)

    #CE = Union(up_regex, gene_dm)

    E = Entities(words, gene_dm)

    return E

#Parse document into smaller pieces------------------------------------------------------------------------------------

from itertools import izip_longest

def grouper(n, iterable, fillvalue=None):

    "Collect data into fixed-length chunks or blocks"

    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx

    args = [iter(iterable)] * n

    return izip_longest(fillvalue=fillvalue, *args)

n = 300

with open('AGR2_blood_biomarker.txt') as f:

    for i, g in enumerate(grouper(n, f, fillvalue=''), 1):

        with open('small_file_{0}'.format(i * n), 'w') as fout:

            fout.writelines(g)

#Run-------------------------------------------------------------------------------------------------------------------
def generateBiomarkerCandidates():
    return biomarkerGenerator (parseDocIntoWords())

