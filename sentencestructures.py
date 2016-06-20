from ddlite import *

def getKnownStructures():
    knownStructures = []
    markerDatabase = ["agr2", "psa", "anterior gradient"]
    diseaseDatabase = ["crpc", "prostate cancer", "prostate cancer cells", "ne-crpc", "metastatic", "metastatic prostate cancer", "crpc-ne"]
    MAX_DISTANCE = 10
    def distanceToNearestWord(spot, wordList, type):
        importantList = []
        if type == "marker":
            importantList = diseaseDatabase
        else:
            importantList = markerDatabase
        counter = spot + 1
        word = wordList[counter]
        print counter
        while not word in importantList and counter < len(wordList):
            # print word  + "  |  " + str(counter)
            word = wordList[counter]
            counter += 1
        return counter - spot

    filename = "AGR2_blood_biomarker.txt"
    text = open(filename, "r").read()
    print "OPENING FILE"
    # print text
    sentence_parser = SentenceParser()
    list = sentence_parser.parse(text)
    print "PARSED TEXT"
    words = []
    print "GETTING ALL WORDS"
    for sentence in list:
        i = 0
        while i < len(sentence.words):
            word = sentence.words[i]
            if(sentence.dep_labels[i] == "compound"):
                while(sentence.dep_labels[i] == "compound"):
                    i += 1
                    word += " " + sentence.words[i]
            words.append(word.lower())
            i += 1

        # for word in sentence.words:
        #     words.append(word)
    print words
    print "GETTING BASIC STRUCTURES"
    count = 0
    while count < len(words):
        word = words[count]
        if word in markerDatabase:
            print "FOUND " + word
            distance = distanceToNearestWord(count, words, "marker")
            print "DISTANCE FOUND TO BE " + str(distance)
            if distance < MAX_DISTANCE:
                basicStructure = ""
                for word in words[count + 1:count+distance - 1]:
                    basicStructure += " " + word
                knownStructures.append(basicStructure)
                print "FOUND STRUCTURE: " + basicStructure
            count += distance - 1
        elif word in diseaseDatabase:
            distance = distanceToNearestWord(count, words, "disease")
            if distance < MAX_DISTANCE:
                basicStructure = ""
                for word in words[count + 1:count + distance - 1]:
                    basicStructure += " " +  word
                knownStructures.append(basicStructure)
                print "FOUND STRUCTURE: " + basicStructure
            count += distance - 1
        count += 1
    return knownStructures
print getKnownStructures()