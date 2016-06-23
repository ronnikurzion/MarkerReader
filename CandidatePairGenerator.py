from ddlite import *
import BiomarkerCandidateGenerator, DiseaseCandidateGenerator
def doEverything():
    parser = DocParser('AGR2_blood_biomarker.txt', ftreader=TextReader())
    sentences = parser.parseDocSentences()

    BM = BiomarkerCandidateGenerator.generateBiomarkerCandidates()
    DM = DiseaseCandidateGenerator.generateDiseaseCandidates()

    possiblePairs = Relations(sentences, BM, DM)
    feats = possiblePairs.extract_features()
    otherModel = DDLiteModel(possiblePairs, feats)


    #1
    def LF_distance(m):
        distance = abs(m.e2_idxs[0] - m.e1_idxs[0])
        if distance < 10:
            # print "RETURNING ONE"
            return 1
        else:
            return 0
    #7
    def LF_associate(m):
       if ('associate' in m.post_window1('lemmas')) and ('associate' in m.pre_window2('lemmas')) :
           return 1
       else:
           return 0
    #8
    def LF_express(m):
        return 1 if ('express' in m.post_window1('lemmas')) and ('express' in m.pre_window2('lemmas')) else 0
    #9
    def LF_marker(m):
        return 1 if('marker' in m.post_window1('lemmas') or 'biomarker' in m.post_window1('lemmas')) and ('marker' in m.post_window2('lemmas') or 'biomarker' in m.post_window2('lemmas')) else 0
    #10
    def LF_elevated(m):
            return 1 if ('elevated' in m.post_window1('lemmas')) and ('elevated' in m.pre_window2('lemmas')) else 0
    def LF_decreased(m):
            return 1 if ('decreased' in m.post_window1('lemmas')) and ('decreased' in m.pre_window2('lemmas')) else 0
    #11
    def LF_correlation(m):
        return 1 if ('correlation' in m.pre_window1('lemmas')) else 0
    #12
    def LF_correlate(m):
        return 1 if ('correlates' in m.post_window1('lemmas')) and ('found' in m.pre_window2('lemmas')) else 0
    #13
    def LF_found(m):
        return 1 if ('found' in m.post_window1('lemmas')) and ('found' in m.pre_window2('lemmas')) else 0







    LFs = [LF_distance, LF_associate, LF_express, LF_marker, LF_elevated, LF_decreased, LF_correlation, LF_correlate, LF_found]
    gt = None
    uids = None
    otherModel.open_mindtagger(num_sample=100, width='100%', height=1200)
    input = raw_input("FISH")
    otherModel.add_mindtagger_tags()
    otherModel.update_gt(gt[50:], uids=uids[50:])

    # otherModel.apply_lfs(LFs, clear=False)
    return otherModel
    # """DEBUGGING CODE"""
    # otherModel.open_mindtagger(num_sample=100, width='100%', height=1200)
    # otherModel.add_mindtagger_tags()
    # otherModel.plot_lf_stats()
    #
    # """END"""
# # with open("thing.xml", "wb") as f:
#
# doEverything()