from Parser.auxiliary import *


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
            self.ICT_AVG = ICT_Z if ICT_A == NA else ICT_A
        else:
            self.ICT_AVG = (ICT_A + ICT_Z)/2
        self.ICT_MIN = min(ICT_A, ICT_Z)
        self.ICT_MAX = max(ICT_A, ICT_Z)

        # Slope lists:
        # Level1: (height1-height2 / age1-age2)
        # Level2: (height1-height3 / age1-age3) : non-adjacent samples
        self.heightToAgeLevel1 = []
        self.heightToAgeLevel2 = []
        self.weightToAgeLevel1 = []
        self.weightToAgeLevel2 = []
        self.bmiToAgeLevel1 = []
        self.bmiToAgeLevel2 = []

        #Naive ICT check on swedish children - Step 1
        self.heightToAgeBurst = []

        # Samples:
        self.goodSamples = []
        self.badSamples = []

    def addSample(self, s, missing = False): #virtual function
        pass

    def calculateBurst(self):
        for x, y, z in zip(self.goodSamples, self.goodSamples[1:],self.goodSamples[2:]):
            self.heightToAgeBurst.append(y.age, ((z.height / y.height) - (y.height / x.height)))
    def calculateSlops(self):
        for x, y in zip(self.goodSamples, self.goodSamples[1:]):
            self.heightToAgeLevel1.append(y.height - x.height)
            self.weightToAgeLevel1.append(y.weight - x.weight)
            self.bmiToAgeLevel1.append(y.BMI - x.BMI)
        for x, y in zip(self.goodSamples, self.goodSamples[2:]):
            self.heightToAgeLevel2.append(y.height - x.height)
            self.weightToAgeLevel2.append(y.weight - x.weight)
            self.bmiToAgeLevel2.append(y.BMI - x.BMI)

    def getNumberOfSampls(self, missing=False):
        if missing==False:
            return len(self.goodSamples)
        return len(self.badSamples)
