import pickle, os, sys, re
import unicodedata
from ddlite import *
def generateDiseaseCandidates():

    with open('diseaseDatabase.pickle', 'rb') as f:
        diseaseDictionary = pickle.load(f)
    with open('diseaseAbbreviationsDatabase.pickle', 'rb') as f:
       diseaseAbb = pickle.load(f)

    filename = "AGR2_blood_biomarker.txt"
    text = open(filename, "r").read()

    otherparser = DocParser('AGR2_blood_biomarker.txt', ftreader =  TextReader())
    words = otherparser.parseDocSentences()

    DiseaseMatch = DictionaryMatch(label = "Diseases", dictionary = diseaseDictionary, ignore_case= True)
    AbbMatch = DictionaryMatch(label = "Abb", dictionary = diseaseAbb, ignore_case = False)

    _DME = Entities(words, DiseaseMatch)
    AbbE = Entities(words, AbbMatch)

    EE = Entities(words, DiseaseMatch)

    editedText = addDiseaseBases(EE,_DME,text)
    editedWords = words

    sentence_parser = SentenceParser()
    list = sentence_parser.parse(editedText, 1)
    for sentence in list:
        editedWords.append(sentence)

    newEE = Entities(editedWords,DiseaseMatch)

    return newEE





def addDiseaseBases(EE, diseaseDictionary, final_article_str):
    counter = 0
    listCounter = 0
    wordIndex = 0
    currentPos = ''
    disease_candidates_edits = []
    for entity in EE:
        disease_index = entity.idxs[0]
        if disease_index is not 0 :
            sentenceWords = entity.pre_window(attribute='words', n=disease_index)
            diseaseName = unicodedata.normalize('NFKD', ' '.join(entity.mention(attribute='words'))).encode('ascii', 'ignore')
            sentencePos = entity.pre_window(attribute='poses', n=disease_index)
            normalized_Pos = unicodedata.normalize('NFKD', sentencePos[0]).encode('ascii','ignore')
            if normalized_Pos == 'CC':
                disease_base = ' ' + entity.mention(attribute='words')[len(entity.idxs) - 1] + ' '  # get base of disease(tumor,cancer)
                normalized_disease_base = unicodedata.normalize('NFKD', disease_base).encode('ascii','ignore')
                sentenceWords.reverse()
                joined_sentenceWords = ' '.join(sentenceWords)
                normalized_sentenceWords = unicodedata.normalize('NFKD', joined_sentenceWords).encode('ascii', 'ignore')
                normalized_unjoined_sentenceWords = []
                for sentence in sentenceWords:
                    normalized_sentence = unicodedata.normalize('NFKD', sentence).encode('ascii', 'ignore')
                    normalized_unjoined_sentenceWords.append(normalized_sentence)
                cutSentence = ' '.join(sentenceWords[0:len(sentenceWords) - 1])
                normalized_cutSentence = unicodedata.normalize('NFKD', cutSentence).encode('ascii','ignore')
                sentenceIdx = substringIndex(final_article_str, normalized_unjoined_sentenceWords)
                indicesOfAnd = [(m.start(0)) for m in re.finditer('and', normalized_sentenceWords)]
                numberOfCommas = len([(m.start(0)) for m in re.finditer(',', normalized_sentenceWords)]) #commas add one extra whitespace
                editIdx = sentenceIdx + indicesOfAnd[len(indicesOfAnd)-1] - numberOfCommas #add sentence Index + Index of And - 1 - number of commas
                for disease_candidate in diseaseDictionary:
                    disease_candidate_name = ' '.join(disease_candidate.mention(attribute='words')) #take unicode array of disease name and join
                    normalized_disease_candidate_name = unicodedata.normalize('NFKD', disease_candidate_name).encode('ascii','ignore')
                    if normalized_disease_candidate_name.lower() in (normalized_cutSentence + normalized_disease_base).lower():
                        disease_candidates_edits.append([editIdx, normalized_cutSentence, normalized_disease_base]) #EDITED
                        listCounter = listCounter + 1
        counter = counter + 1
    disease_candidates_edits = removeRepeats(disease_candidates_edits)
    disease_candidates_edits.sort()
    disease_candidates_edits.reverse() #reverse so that we edit the article back-front to avoid index errors
    counter = 0 ;
    for edit in disease_candidates_edits:
        edit_str_addition = edit[2]
        edit_index = edit[0]
        final_article_str = final_article_str[0:edit_index] + edit_str_addition + final_article_str[edit_index:len(final_article_str)]
        counter = counter + 1
    return final_article_str


def substringIndex(text, listWords):
    end = -3
    candidate_index = -2
    word = listWords[0]
    allIndices = [m.start() for m in re.finditer(word, text)]
    for index in allIndices:
        end = substringIndex_help(text, listWords, index)
        if (end is not -1 and end is not None):
            candidate_index = index
            return candidate_index

    return candidate_index


def substringIndex_help(text, listWords, index):
    if len(listWords) is 0 :
        return 0
    elif len(listWords) is 1:
        withinRange = text[index:index + 15 + len(listWords[0])]
        if listWords[0] in withinRange:
            index = withinRange.index(listWords[0])
            return substringIndex_help(text,[],index)
        else:
            return -1
    else:
        parsedPaper = text[index:]
        withinRange = text[index:index+len(listWords[0]) + 15 + len(listWords[1])]
        if listWords[1] in withinRange:
            index = withinRange.index(listWords[1])
            return substringIndex_help(parsedPaper,listWords[1:],index)
        else:
            return -1

def removeRepeats (list):
    counter = 1
    case = None
    for edit in list :
        for check in list[counter:] :
            if edit[0] is check[0]:     #If the two objects have the same edit index
                list.remove(check)
            counter = counter + 1
    return list







generateDiseaseCandidates()




