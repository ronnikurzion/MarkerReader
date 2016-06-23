from ddlite import *
import BioMarkerCandidateGenerator, DiseaseCandidateGenerator


def doEverything():
    parser = DocParser('AGR2_blood_biomarker.txt', ftreader=TextReader())
    sentences = parser.parseDocSentences()

    BM = BioMarkerCandidateGenerator.generateBiomarkerCandidates()
    DM = DiseaseCandidateGenerator.generateDiseaseCandidates()

    possiblePairs = Relations(sentences, BM, DM)
    feats = possiblePairs.extract_features()
    otherModel = DDLiteModel(possiblePairs, feats)

    # 1
    def LF_distance(m):
        distance = abs(m.e2_idxs[0] - m.e1_idxs[0])
        if distance < 10:
            # print "RETURNING ONE"
            return 1
        else:
            return 0
    # 2
    def LF_associate(m):
        if ('associate' in m.post_window1('lemmas')) and ('associate' in m.pre_window2('lemmas')):
            return 1
        else:
            return 0
    # 3
    def LF_express(m):
        return 1 if ('express' in m.post_window1('lemmas')) and ('express' in m.pre_window2('lemmas')) else 0
    # 4
    def LF_marker(m):
        return 1 if ('marker' in m.post_window1('lemmas') or 'biomarker' in m.post_window1('lemmas')) and (
        'marker' in m.post_window2('lemmas') or 'biomarker' in m.post_window2('lemmas')) else 0
    # 5
    def LF_elevated(m):
        return 1 if ('elevated' in m.post_window1('lemmas')) and ('elevated' in m.pre_window2('lemmas')) else 0
    def LF_decreased(m):
        return 1 if ('decreased' in m.post_window1('lemmas')) and ('decreased' in m.pre_window2('lemmas')) else 0
    # 6
    def LF_correlation(m):
        return 1 if ('correlation' in m.pre_window1('lemmas')) else 0
    # 7
    def LF_correlate(m):
        return 1 if ('correlates' in m.post_window1('lemmas')) and ('found' in m.pre_window2('lemmas')) else 0
    # 8
    def LF_found(m):
        return 1 if ('found' in m.post_window1('lemmas')) and ('found' in m.pre_window2('lemmas')) else 0
    # 9 (-1 if biomarker is confused with a name of a person)
    def LF_People(m):
        return -1 if ('NNP' in mention1(attribute='poses')) else 0
    #10
    def LF_diagnosed(m):
        return 1 if('diagnose' in m.post_window1('lemmas')) else 0
    #11
    def LF_variant(m):
        return 1 if('variant of' in m.pre_window1('lemmas')) else 0
    #12
    def LF_appear(m):
        return 1 if ('appear' in m.post_window1('lemmas')) else 0
    #13
    def LF_connect(m):
        return 1 if ('connect' in m.post_window1('lemmas')) else 0
    #14
    def LF_relate(m):
        return 1 if ('relate' in m.post_window1('lemmas')) else 0
    #15
    def LF_exhibit(m):
        return 1 if ('exhibit' in m.post_window1('lemmas')) else 0
    #16
    def LF_indicate(m):
        return 1 if ('indicate' in m.post_window1('lemmas')) else 0
    #17
    def LF_signify(m):
        return 1 if ('signify' in m.post_window1('lemmas')) else 0
    #18
    def LF_show(m):
        return 1 if ('show' in m.post_window1('lemmas')) else 0
    #19
    def LF_demonstrate(m):
        return 1 if ('demonstrate' in m.post_window1('lemmas')) else 0
    #20
    def LF_reveal(m):
        return 1 if ('reveal' in m.post_window1('lemmas')) else 0
    #21
    def LF_suggest(m):
        return 1 if ('suggest' in m.post_window1('lemmas')) else 0
    #22
    def LF_evidence(m):
        return 1 if ('evidence for' in m.post_window1('lemmas')) else 0
    #23
    def LF_indication(m):
        return 1 if ('indication of' in m.post_window1('lemmas')) else 0
    #24
    def LF_elevation(m):
        return 1 if ('elevation' in m.post_window1('lemmas')) else 0
    #25
    def LF_diagnosis(m):
        return 1 if ('diagnosis of' in m.post_window1('lemmas')) else 0
    #26
    def LF_variation(m):
        return 1 if ('variation of' in m.pre_window1('lemmas')) else 0
    #27
    def LF_modification(m):
        return 1 if ('modification of' in m.pre_window1('lemmas')) else 0
    #28
    def LF_suggestion(m):
        return 1 if ('suggestion' in m.post_window1('lemmas')) else 0
    #29
    def LF_link(m):
        return 1 if ('link' in m.post_window1('lemmas')) else 0
    #30
    def LF_derivation(m):
        return 1 if ('derivation of' in m.pre_window1('lemmas')) else 0
    #31
    def LF_elevation(m):
        return 1 if ('elevation' in m.post_window1('lemmas')) else 0
    #32
    def LF_denote(m):
        return 1 if ('denote' in m.post_window1('lemmas')) else 0
    #33
    def LF_denotation(m):
        return 1 if ('denotation' in m.post_window1('lemmas')) else 0
    #34
    def LF_demonstration(m):
        return 1 if ('demonstration' in m.post_window1('lemmas')) else 0
    


    LFs = [LF_distance, LF_associate, LF_express, LF_marker, LF_elevated, LF_decreased, LF_correlation, LF_correlate,
           LF_found]
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
