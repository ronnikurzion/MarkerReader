import pickle, os, sys
from ddlite import *
def generateDiseaseCandidate():
    words = []
    with open('database.pickle', 'rb') as f:
        diseases = pickle.load(f)

    dp = DocParser('AGR2_blood_biomarker.txt', ftreader =  TextReader())
    words = dp.parseDocSentences()

    DiseaseMatch = DictionaryMatch(label = "Diseases", dictionary = diseases, ignore_case= False)

    EE = Entities(words, DiseaseMatch)
    return EE



