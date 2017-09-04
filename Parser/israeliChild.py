from Parser.auxiliary import *
from Parser.child import Child
from Parser.sample import IsraeliSample
from Utility import find_nearest
import numpy as np
from pygrowup import Calculator
import pygrowup
from numpy import mean as avg

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

        self.avg_HCToAgeLevel1 = NA
        self.avg_HCToAgeLevel2 = NA
        self.avg_HCdivHeightLevel1 = NA
        self.avg_HCdivHeightLevel2 = NA
        self.avg_HCdivHeightSqLevel1 = NA
        self.avg_HCdivHeightSqLevel2 = NA
        self.avg_HCdivWeightLevel1 = NA
        self.avg_HCdivWeightLevel2 = NA
        self.avg_HCdivWeightSqLevel1 = NA
        self.avg_HCdivWeightSqLevel2 = NA
        self.max_HCToAgeLevel1 = NA
        self.max_HCToAgeLevel2 = NA
        self.max_HCdivHeightLevel1 = NA
        self.max_HCdivHeightLevel2 = NA
        self.max_HCdivHeightSqLevel1 = NA
        self.max_HCdivHeightSqLevel2 = NA
        self.max_HCdivWeightLevel1 = NA
        self.max_HCdivWeightLevel2 = NA
        self.max_HCdivWeightSqLevel1 = NA
        self.max_HCdivWeightSqLevel2 = NA
        self.min_HCToAgeLevel1 = NA
        self.min_HCToAgeLevel2 = NA
        self.min_HCdivHeightLevel1 = NA
        self.min_HCdivHeightLevel2 = NA
        self.min_HCdivHeightSqLevel1 = NA
        self.min_HCdivHeightSqLevel2 = NA
        self.min_HCdivWeightLevel1 = NA
        self.min_HCdivWeightLevel2 = NA
        self.min_HCdivWeightSqLevel1 = NA
        self.min_HCdivWeightSqLevel2 = NA

    def addBrother(self, brother):
        self.brothers.add(brother)

    def updateYear(self, year):
        self.birthYear = year

    def calculateSlops(self):
        super(IsraeliChild, self).calculateSlops()
        self.calculateHeadSlops()

    def calculateHeadSlops(self):
        goodSamples = [s for s in self.goodSamplesWithHC if s.age > 0.35]
        for x, y in zip(goodSamples, goodSamples[1:]):
            if y.age == x.age:
                continue
            self.HCToAgeLevel1.append((y.HC - x.HC)/(y.age - x.age))
            self.HCdivHeightLevel1.append((y.HCdivHeight - x.HCdivHeight)/(y.age - x.age))
            self.HCdivHeightSqLevel1.append((y.HCdivHeightSq - x.HCdivHeightSq)/(y.age - x.age))
            self.HCdivWeightLevel1.append((y.HCdivWeight - x.HCdivWeight)/(y.age - x.age))
            self.HCdivWeightSqLevel1.append((y.HCdivWeightSq - x.HCdivWeightSq)/(y.age - x.age))
        for x, y in zip(goodSamples, goodSamples[2:]):
            if y.age == x.age:
                continue
            self.HCToAgeLevel2.append((y.HC - x.HC)/(y.age - x.age))
            self.HCdivHeightLevel2.append((y.HCdivHeight - x.HCdivHeight)/(y.age - x.age))
            self.HCdivHeightSqLevel2.append((y.HCdivHeightSq - x.HCdivHeightSq)/(y.age - x.age))
            self.HCdivWeightLevel2.append((y.HCdivWeight - x.HCdivWeight)/(y.age - x.age))
            self.HCdivWeightSqLevel2.append((y.HCdivWeightSq - x.HCdivWeightSq)/(y.age - x.age))

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

    # Parameters for regression decision tree
    # Returns features vector, data vector and ICT classification
    def generateParametersForRegressionDecisionTree(self, common_ages, first=True):
        features, data, self.autoICT = super(IsraeliChild, self).generateParametersForRegressionDecisionTree(common_ages, first)
        if self.autoICT == NA:
            return [], [], 0
        for age in common_ages:
            features += ["HC at %s" % str(age)]
            i = find_nearest([a.age for a in self.goodSamplesWithHC], age)
            if abs(self.goodSamples[i].age - age) > 5 / MONTHS:
                data += [np.nan]
            else:
                data += [self.goodSamplesWithHC[i].HC]

        features += ["HC at 6 months", "HC at 6 months Avg'd"]
        if self.goodSamplesWithHC:
            smi_HC = find_nearest([a.age for a in self.goodSamplesWithHC], 0.5)
            data += [(self.goodSamplesWithHC[smi_HC]).HC]
            if len(self.goodSamplesWithHC) > smi_HC + 1:
                data += [((self.goodSamplesWithHC[smi_HC - 1]).HC +
                          (self.goodSamplesWithHC[smi_HC]).HC +
                          (self.goodSamplesWithHC[smi_HC + 1]).HC) / 3]
            else:
                data += [(self.goodSamplesWithHC[smi_HC]).HC]

        features += ["Avg brothers HC at 6 months (m)"]
        b_smi_HC = [find_nearest([a.age for a in x.goodSamplesWithHC], 0.5) if len(x.goodSamplesWithHC) else NA for x in
                    self.brothers] #when refactoring stayes here
        if NA not in b_smi_HC:
            data += [np.mean([list(self.brothers)[i].goodSamplesWithHC[b_smi_HC[i]].HC for i in range(0, len(b_smi_HC))])]
        else:
            data += [np.nan]

        features += ["avg of HCToAgeLevel1", "max of HCToAgeLevel1", "min of HCToAgeLevel1", "avg of HCToAgeLevel2",
                     "max of HCToAgeLevel2", "min of HCToAgeLevel2", "avg of HCdivHeightLevel1",
                     "max of HCdivHeightLevel1", "min of HCdivHeightLevel1", "avg of HCdivHeightLevel2",
                     "max of HCdivHeightLevel2", "min of HCdivHeightLevel2", "avg of HCdivHeightSqLevel1",
                     "max of HCdivHeightSqLevel1", "min of HCdivHeightSqLevel1", "avg of HCdivHeightSqLevel2",
                     "max of HCdivHeightSqLevel2", "min of HCdivHeightSqLevel2", "avg of HCdivWeightLevel1",
                     "max of HCdivWeightLevel1", "min of HCdivWeightLevel1", "avg of HCdivWeightLevel2",
                     "max of HCdivWeightLevel2", "min of HCdivWeightLevel2", "avg of HCdivWeightSqLevel1",
                     "max of HCdivWeightSqLevel1", "min of HCdivWeightSqLevel1", "avg of HCdivWeightSqLevel2",
                     "max of HCdivWeightSqLevel2", "min of HCdivWeightSqLevel2"]

        data += [self.avg_HCToAgeLevel1, self.max_HCToAgeLevel1, self.min_HCToAgeLevel1, self.avg_HCToAgeLevel2,
                 self.max_HCToAgeLevel2, self.min_HCToAgeLevel2, self.avg_HCdivHeightLevel1, self.max_HCdivHeightLevel1,
                 self.min_HCdivHeightLevel1, self.avg_HCdivHeightLevel2, self.max_HCdivHeightLevel2,
                 self.min_HCdivHeightLevel2, self.avg_HCdivHeightSqLevel1, self.max_HCdivHeightSqLevel1,
                 self.min_HCdivHeightSqLevel1, self.avg_HCdivHeightSqLevel2, self.max_HCdivHeightSqLevel2,
                 self.min_HCdivHeightSqLevel2, self.avg_HCdivWeightLevel1, self.max_HCdivWeightLevel1,
                 self.min_HCdivWeightLevel1, self.avg_HCdivWeightLevel2, self.max_HCdivWeightLevel2,
                 self.min_HCdivWeightLevel2, self.avg_HCdivWeightSqLevel1, self.max_HCdivWeightSqLevel1,
                 self.min_HCdivWeightSqLevel1, self.avg_HCdivWeightSqLevel2, self.max_HCdivWeightSqLevel2,
                 self.min_HCdivWeightSqLevel2]

        features, data = self.generateWHOparameters(common_ages, features, data)

        features += ["nation"]
        data += [Nationality.ISR.value]

        if first:
            features += ["fatherAge (Years)", "motherWeight (KG)", "motherHeight (M)"]
            data += [self.fatherAge, self.motherWeight, self.motherHeight/METER]

        return features, data, self.autoICT

    def generateWHOparameters(self, common_ages, features, data):
        features, data = super(IsraeliChild, self).generateWHOparameters(common_ages, features, data)
        calculator = Calculator(adjust_height_data=False, adjust_weight_scores=False,
                                include_cdc=False, logger_name='pygrowup',
                                log_level='INFO')
        common_ages = common_ages[1:8]
        for age in common_ages:
            i = find_nearest([a.age for a in self.goodSamples], age)
            s = self.goodSamples[i]
            child_age, height, hc = str(self.goodSamples[i].age * MONTHS), str(
                self.goodSamples[i].height * METER), str(self.goodSamples[i].HC)
            sex = 'M' if self.sex == 1 else 'F'
            features += ["WHO hcfa z-score at %s" % str(age)]
            try:
                data += [calculator.hcfa(hc, child_age, sex, height)]
            except Exception as e:
                    data += [np.nan]
        return features, data

    def setValuesOfSlopeVectors(self):
        super(IsraeliChild, self).setValuesOfSlopeVectors()
        if len(self.HCToAgeLevel1) > 0:
            self.avg_HCToAgeLevel1 = avg(self.HCToAgeLevel1)
            self.max_HCToAgeLevel1 = max(self.HCToAgeLevel1)
            self.min_HCToAgeLevel1 = min(self.HCToAgeLevel1)
        if len(self.HCToAgeLevel2) > 0:
            self.avg_HCToAgeLevel2 = avg(self.HCToAgeLevel2)
            self.max_HCToAgeLevel2 = max(self.HCToAgeLevel2)
            self.min_HCToAgeLevel2 = min(self.HCToAgeLevel2)
        if len(self.HCdivHeightLevel1) > 0:
            self.avg_HCdivHeightLevel1 = avg(self.HCdivHeightLevel1)
            self.max_HCdivHeightLevel1 = max(self.HCdivHeightLevel1)
            self.min_HCdivHeightLevel1 = min(self.HCdivHeightLevel1)
        if len(self.HCdivHeightLevel2) > 0:
            self.avg_HCdivHeightLevel2 = avg(self.HCdivHeightLevel2)
            self.max_HCdivHeightLevel2 = max(self.HCdivHeightLevel2)
            self.min_HCdivHeightLevel2 = min(self.HCdivHeightLevel2)
        if len(self.HCdivHeightSqLevel1) > 0:
            self.avg_HCdivHeightSqLevel1 = avg(self.HCdivHeightSqLevel1)
            self.max_HCdivHeightSqLevel1 = max(self.HCdivHeightSqLevel1)
            self.min_HCdivHeightSqLevel1 = min(self.HCdivHeightSqLevel1)
        if len(self.HCdivHeightSqLevel2) > 0:
            self.avg_HCdivHeightSqLevel2 = avg(self.HCdivHeightSqLevel2)
            self.max_HCdivHeightSqLevel2 = max(self.HCdivHeightSqLevel2)
            self.min_HCdivHeightSqLevel2 = min(self.HCdivHeightSqLevel2)
        if len(self.HCdivWeightLevel1) > 0:
            self.avg_HCdivWeightLevel1 = avg(self.HCdivWeightLevel1)
            self.max_HCdivWeightLevel1 = max(self.HCdivWeightLevel1)
            self.min_HCdivWeightLevel1 = min(self.HCdivWeightLevel1)
        if len(self.HCdivWeightLevel2) > 0:
            self.avg_HCdivWeightLevel2 = avg(self.HCdivWeightLevel2)
            self.max_HCdivWeightLevel2 = max(self.HCdivWeightLevel2)
            self.min_HCdivWeightLevel2 = min(self.HCdivWeightLevel2)
        if len(self.HCdivWeightSqLevel1) > 0:
            self.avg_HCdivWeightSqLevel1 = avg(self.HCdivWeightSqLevel1)
            self.max_HCdivWeightSqLevel1 = max(self.HCdivWeightSqLevel1)
            self.min_HCdivWeightSqLevel1 = min(self.HCdivWeightSqLevel1)
        if len(self.HCdivWeightSqLevel2) > 0:
            self.avg_HCdivWeightSqLevel2 = avg(self.HCdivWeightSqLevel2)
            self.max_HCdivWeightSqLevel2 = max(self.HCdivWeightSqLevel2)
            self.min_HCdivWeightSqLevel2 = min(self.HCdivWeightSqLevel2)

    def __repr__(self):
        if len(self.id) == 2:
            return 'IsraeliChild(id=%s, %s)' % (self.id)
        else:
            return 'IsraeliChild(id=%s, %s, %s)' % (self.id)