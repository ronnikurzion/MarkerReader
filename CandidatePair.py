class CandidatePair:
    biomarker = None
    disease = None

    def __init__(self, biomarker, disease):
        self.biomarker = biomarker
        self.disease = disease

    def __repr__(self):
        return "Biomarker: " + self.biomarker + " Disease: " + self.disease


