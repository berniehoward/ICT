from constants import *

class Child:

    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z):

        # General info:
        self.id = id
        self.sex = sex
        self.birthWeight = birthWeight
        self.birthHeight = birthHeight
        self.gestationalAge = gestationalAge

        # ICT info:
        if ICT_A == NA and ICT_Z == NA:
            self.ICT_AVG = NA
        elif ICT_A == NA or ICT_Z == NA:
            ICT_AVG = ICT_Z if ICT_A == NA else ICT_A
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
        self.goodSamples = []
        self.badSamples = []

    def addSample(self, sample, missing = False):
        if missing == False:
            self.goodSamples.append(sample)
        else:
            self.badSamples.append(sample)

    def calculateSlops(self):
        pass

