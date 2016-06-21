from ddlite import *
import BiomarkerCandidateGenerator, DiseaseCandidateGenerator

dp = DocParser('AGR2_blood_biomarker.txt', ftreader=TextReader())
sentences = dp.parseDocSentences()

BM = BiomarkerCandidateGenerator.generateBiomarkerCandidates()
DM = DiseaseCandidateGenerator.generateDiseaseCandidates()

R = Relations(sentences, BM, DM)
feats = R.extract_features()
DDL = DDLiteModel(R, feats)
DDL.open_mindtagger(num_sample=100, width='100%', height=1200)
input = raw_input("HOLA?")
