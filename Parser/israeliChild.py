from Parser.auxiliary import *
from Parser.child import Child
from Parser.sample import IsraeliSample
from Utility import find_nearest
import numpy as np
season = [NA, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 0, 0]  # winter, spring, summer, fall
ISR = '0' # nation symbol for regression tree

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
        features = ["sex", "nation", "birthWeight (KG)", "birthHeight (M)", "gestationalAge (Weeks)",
                "birthPosition", "birthYear", "birthMonth", "season", "preterm flag",
                "max_weightToAgeLevel1", "max_weightDivAgeLevel1", "min_weightToAgeLevel1",
                "min_weightDivAgeLevel1", "avg_weightToAgeLevel1", "avg_weightDivAgeLevel1",
                "max_weightToAgeLevel2", "max_weightDivAgeLevel2", "min_weightToAgeLevel2",
                "min_weightDivAgeLevel2", "avg_weightToAgeLevel2", "avg_weightDivAgeLevel2",
                "max_heightToAgeLevel1", "max_heightDivAgeLevel1", "min_heightToAgeLevel1",
                "min_heightDivAgeLevel1", "avg_heightToAgeLevel1", "avg_heightDivAgeLevel1",
                "max_heightToAgeLevel2", "max_heightDivAgeLevel2", "min_heightToAgeLevel2",
                "min_heightDivAgeLevel2", "avg_heightToAgeLevel2", "avg_heightDivAgeLevel2",
                "max_BMIToAgeLevel1", "max_BMIDivAgeLevel1", "min_BMIToAgeLevel1",
                "min_BMIDivAgeLevel1", "avg_BMIToAgeLevel1", "avg_BMIDivAgeLevel1",
                "max_BMIToAgeLevel2", "max_BMIDivAgeLevel2", "min_BMIToAgeLevel2",
                "min_BMIDivAgeLevel2", "avg_BMIToAgeLevel2", "avg_BMIDivAgeLevel2",
                "Height at 6 months (m)", "Weight at 6 months (KG)", "HC at 6 months",
                "Height at 6 months (m) Avg'd", "Weight at 6 months (KG) Avg'd", "HC at 6 months Avg'd",
                "Avg brothers Height at 6 months (m)" , "Avg brothers Weight at 6 months (m)",
                "Avg brothers HC at 6 months (m)"]
        data = [self.sex, 0, self.birthWeight/KILO, self.birthHeight, self.gestationalAge,
                self.position, self.birthYear, self.birthMonth, self.season, self.preterm,
                self.max_weightToAgeLevel1, self.max_weightDivAgeLevel1, self.min_weightToAgeLevel1,
                self.min_weightDivAgeLevel1,self.avg_weightToAgeLevel1, self.avg_weightDivAgeLevel1,
                self.max_weightToAgeLevel2, self.max_weightDivAgeLevel2, self.min_weightToAgeLevel2,
                self.min_weightDivAgeLevel2, self.avg_weightToAgeLevel2, self.avg_weightDivAgeLevel2,
                self.max_heightToAgeLevel1, self.max_heightDivAgeLevel1, self.min_heightToAgeLevel1,
                self.min_heightDivAgeLevel1, self.avg_heightToAgeLevel1, self.avg_heightDivAgeLevel1,
                self.max_heightToAgeLevel2, self.max_heightDivAgeLevel2, self.min_heightToAgeLevel2,
                self.min_heightDivAgeLevel2, self.avg_heightToAgeLevel2, self.avg_heightDivAgeLevel2,
                self.max_bmiToAgeLevel1, self.max_bmiDivAgeLevel1, self.min_bmiToAgeLevel1,
                self.min_bmiDivAgeLevel1, self.avg_bmiToAgeLevel1, self.avg_bmiDivAgeLevel1,
                self.max_bmiToAgeLevel2, self.max_bmiDivAgeLevel2, self.min_bmiToAgeLevel2,
                self.min_bmiDivAgeLevel2, self.avg_bmiToAgeLevel2, self.avg_bmiDivAgeLevel2]
        if self.goodSamples:
            smi = find_nearest([a.age for a in self.goodSamples], 0.5)
            smi_HC = find_nearest([a.age for a in self.goodSamplesWithHC], 0.5)
            data += [(self.goodSamples[smi]).height,
                     (self.goodSamples[smi]).weight,
                     (self.goodSamplesWithHC[smi_HC]).HC,
                     ((self.goodSamples[smi-1]).height+(self.goodSamples[smi]).height+(self.goodSamples[smi+1]).height) / 3,
                     ((self.goodSamples[smi - 1]).weight + (self.goodSamples[smi]).weight + (self.goodSamples[smi + 1]).weight) / 3,
                     ((self.goodSamplesWithHC[smi_HC-1]).HC+(self.goodSamplesWithHC[smi_HC]).HC+(self.goodSamplesWithHC[smi_HC+1]).HC) / 3]

        b_smi = [find_nearest([a.age for a in x.goodSamples], 0.5) if len(x.goodSamples) else NA for x in self.brothers]
        b_smi_HC = [find_nearest([a.age for a in x.goodSamplesWithHC], 0.5) if len(x.goodSamplesWithHC) else NA for x in self.brothers]
        if NA not in b_smi:
            data += [np.mean([list(self.brothers)[i].goodSamples[b_smi[i]].height for i in range(0, len(b_smi))]),
                     np.mean([list(self.brothers)[i].goodSamples[b_smi[i]].weight for i in range(0, len(b_smi))]),
                     np.mean([list(self.brothers)[i].goodSamplesWithHC[b_smi_HC[i]].HC for i in range(0, len(b_smi_HC))])]
        else:
            data += [np.nan, np.nan, np.nan]
        # "motherAge (Years)" is only on Test.csv and not on research.csv. possible problem. TODO
        if first:
            features += ["fatherAge (Years)", "motherWeight (KG)", "motherHeight (M)"]
            data += [self.fatherAge, self.motherWeight, self.motherHeight/METER]

        return features, data, self.autoICT

    def __repr__(self):
        if len(self.id) == 2:
            return 'IsraeliChild(id=%s, %s)' % (self.id)
        else:
            return 'IsraeliChild(id=%s, %s, %s)' % (self.id)