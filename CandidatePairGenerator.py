from ddlite import *
import BiomarkerCandidateGenerator, DiseaseCandidateGenerator

parser = DocParser('AGR2_blood_biomarker.txt', ftreader=TextReader())
sentences = parser.parseDocSentences()

BM = BiomarkerCandidateGenerator.generateBiomarkerCandidates()
DM = DiseaseCandidateGenerator.generateDiseaseCandidates()

possiblePairs = Relations(sentences, BM, DM)
feats = possiblePairs.extract_features()
otherModel = DDLiteModel(possiblePairs, feats)
otherModel.open_mindtagger(num_sample=100, width='100%', height=1200)
otherModel.add_mindtagger_tags()
input = raw_input("fasd")