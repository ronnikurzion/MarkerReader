import pickle, os, sys
from ddlite import *
def generateDiseaseCandidates():

    diseaseDictionary = ["prostate cancer"]
    # with open('database.pickle', 'rb') as f:
    #     diseases = pickle.load(f)

    otherparser = DocParser('AGR2_blood_biomarker.txt', ftreader =  TextReader())
    words = otherparser.parseDocSentences()

    DiseaseMatch = DictionaryMatch(label = "Diseases", dictionary = diseaseDictionary, ignore_case= False)

    # EE = Entities(words, DiseaseMatch)
    return DiseaseMatch



