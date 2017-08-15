from Parser.auxiliary import *
from Parser.child import Child
from Parser.sample import IsraeliSample
from Utility import find_nearest

season = [NA, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 0, 0]  # winter, spring, summer, fall


class IsraeliChild(Child):
    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z, \
                 birthPosition, fatherAge, motherAge, motherWeight, motherHeight,
                 birthDate, birthMonth):

        Child.__init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z, birthDate, birthMonth)

        # family related information
        self.position = birthPosition
        self.birthYear = NA
        if fatherAge == '':
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

    def updateYear(self, year):
        self.birthYear = year

    def calculateHeadSlops(self):
        for x, y in zip(self.goodSamplesWithHC, self.goodSamplesWithHC[1:]):
            self.HCToAgeLevel1.append(y.HC - x.HC)
            self.HCdivHeightLevel1.append(y.HCdivHeight - x.HCdivHeight)
            self.HCdivHeightSqLevel1.append(y.HCdivHeightSq - x.HCdivHeightSq)
            self.HCdivWeightLevel1.append(y.HCdivWeight - x.HCdivWeight)
            self.HCdivWeightSqLevel1.append(y.HCdivWeightSq - x.HCdivWeightSq)
        for x, y in zip(self.goodSamplesWithHC, self.goodSamplesWithHC[2:]):
            self.HCToAgeLevel2.append(y.HC - x.HC)
            self.HCdivHeightLevel2.append(y.HCdivHeight - x.HCdivHeight)
            self.HCdivHeightSqLevel2.append(y.HCdivHeightSq - x.HCdivHeightSq)
            self.HCdivWeightLevel2.append(y.HCdivWeight - x.HCdivWeight)
            self.HCdivWeightSqLevel2.append(y.HCdivWeightSq - x.HCdivWeightSq)

    def addSample(self, s, missing=False):
        sample = IsraeliSample(s[0], s[1], s[2], s[3])
        if missing:
            self.badSamples.append(sample)
        else:
            HC = s[3]
            if HC == NA or HC == 0 or HC == '':
                self.goodSamples.append(sample)  # now goodSamples with possible bad HC
            else:
                self.goodSamples.append(sample)
                self.goodSamplesWithHC.append(sample)

    # parameters for regression decision tree
    # returns features vector, data vector and ICT classification
    def generateParametersForRegressionDecisionTree(self, first=True):
        if self.autoICT == NA:
            return [], [], 0
        features = ["sex", "birthWeight (Grams)", "birthHeight (M)", "gestationalAge (Weeks)",
                    "birthPosition", "birthYear", "birthMonth", "season",
                    "preterm flag", "Height at 6 months",
                    "Weight at 6 months", "HC at 6 months"]
        data = [self.sex, self.birthWeight/KILO, self.birthHeight, self.gestationalAge,
                self.position, self.birthYear, self.birthMonth, self.season,
                self.preterm]
        if self.goodSamples:
            six_month_idx = find_nearest([a.age for a in self.goodSamples], 0.5)
            six_month_idx_HC = find_nearest([a.age for a in self.goodSamplesWithHC], 0.5)
            data += [(self.goodSamples[six_month_idx]).height,
                     (self.goodSamples[six_month_idx]).weight,
                     (self.goodSamplesWithHC[six_month_idx_HC]).HC]

        # "motherAge (Years)" is only on Test.csv and not on reasrch.csv. possible problem. TODO
        if first:
            features += ["fatherAge (Years)", "motherWeight (KG)", "motherHeight (M)"]
            data += [self.fatherAge, self.motherWeight, self.motherHeight/METER]

        return features, data, self.autoICT

    def __repr__(self):
        if len(self.id) == 2:
            return 'IsraeliChild(id=%s, %s)' % (self.id)
        else:
            return 'IsraeliChild(id=%s, %s, %s)' % (self.id)