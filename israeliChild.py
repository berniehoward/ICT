from child import Child
from auxiliary import *
season = [0,1,1,1,2,2,2,3,3,3,0,0] #winter, spring, summer, fall
class IsraeliChild(Child):

    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z, \
                 birthPosition, fatherAge, motherAge, motherWeight, motherHeight, \
                 birthMonth, birthYear):

        Child.__init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z)

        #family related information
        self.position = birthPosition

        if self.fatherAge == '':
            self.fatherAge = NA
        else:
            self.fatherAge = fatherAge

        self.motherAge = motherAge
        if motherWeight == '':
            self.motherWeight = NA
            self.motherHeight = NA
        else:
            self.motherWeight = motherWeight
            self.motherHeight = motherHeight

        self.brothers = set()

        self.birthYear = birthYear
        self.birthMonth = birthMonth
        self.season = season[birthMonth]

        self.HCToAgeLevel1 = []
        self.HCToAgeLevel2 = []
        self.HCdivHeightLevel1 = []
        self.HCdivHeightLevel2 = []
        self.HCdivHeightSqLevel1 = []
        self.HCdivHeightSqLevel2 = []
        self.HCdivWeightLevel1 = []
        self.HCdivWeightLevel2 = []
        self.HCdivWeightSqLevel1 = []
        self.HCdivWeightSqLevel2 = []

    def addBrother(self, brother):
        self.brothers.add(brother)

    def calculateHeadSlops(self):
        for x, y in zip(self.goodSamples, self.goodSamples[1:]):
            self.HCToAgeLevel1.append(y.HC - x.HC)
            self.HCdivHeightLevel1.append(y.HCdivHeight - x.HCdivHeight)
            self.HCdivHeightSqLevel1.append(y.HCdivHeightSq - x.HCdivHeightSq)
            self.HCdivWeightLevel1.append(y.HCdivWeight - x.HCdivWeight)
            self.HCdivWeightSqLevel1.append(y.HCdivWeightSq - x.HCdivWeightSq)
        for x, y in zip(self.goodSamples, self.goodSamples[2:]):
            self.HCToAgeLevel2.append(y.HC - x.HC)
            self.HCdivHeightLevel2.append(y.HCdivHeight - x.HCdivHeight)
            self.HCdivHeightSqLevel2.append(y.HCdivHeightSq - x.HCdivHeightSq)
            self.HCdivWeightLevel2.append(y.HCdivWeight - x.HCdivWeight)
            self.HCdivWeightSqLevel2.append(y.HCdivWeightSq - x.HCdivWeightSq)



