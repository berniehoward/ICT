from math import min, max

NA = -100  # value representing we are not able to determine the ICT

class Child:

    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z):

        # General info:
        self.id = id
        self.sex = sex
        self.birthWeight = birthWeight
        self.birthHeight = birthHeight
        self.gestationalAge = gestationalAge

        # ICT info:
        if ICT_A == NA or ICT_Z == NA:
            self.ICT_AVG = NA
        else:
            self.ICT_AVG = (ICT_A + ICT_Z)/2
        self.ICT_MIN = min(ICT_A, ICT_Z)
        self.ICT_MAX = max(ICT_A, ICT_Z)

        # Slope lists:
        # Level1: (height1-height2 / age1-age2)
        # Level2: (height1-height3 / age1-age3) : non-adjacent samples
        self.heightToAgeLevel1 = []
        self.heightToAgeLevel2 = []
        self.wightToAgeLevel1 = []
        self.wightToAgeLevel2 = []
        self.bmiToAgeLevel1 = []
        self.bmiToAgeLevel2 = []

        # Samples:
        self.samples = []

    def addSample(self):
        pass

    def calculateSlops(self):
        pass
