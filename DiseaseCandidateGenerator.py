import pickle, os, sys
from ddlite import *
def generateDiseaseCandidates():

    with open('diseaseDatabase.pickle', 'rb') as f:
        diseaseDictionary = pickle.load(f)
    with open('diseaseAbbreviationsDatabase.pickle', 'rb') as f:
       diseaseAbb = pickle.load(f)


    # otherparser = DocParser('AGR2_blood_biomarker.txt', ftreader =  TextReader())
    # words = otherparser.parseDocSentences()

    DiseaseMatch = DictionaryMatch(label = "Diseases", dictionary = diseaseDictionary, ignore_case= True)
    AbbMatch = DictionaryMatch(label = "Abb", dictionary = diseaseAbb, ignore_case = False)
    Filter = Union(DiseaseMatch, AbbMatch)
    # EE = Entities(words, DiseaseMatch)
    return Filter



