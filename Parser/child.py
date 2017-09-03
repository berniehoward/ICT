from Parser.auxiliary import *
from numpy import mean as avg
from Utility import find_nearest
import numpy as np

season = [NA, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 0, 0]  # winter, spring, summer, fall


class Child:
    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z, birthDate, birthMonth):

        # General info:
        self.id = id
        self.sex = sex
        self.birthWeight = birthWeight
        self.birthHeight = birthHeight
        self.gestationalAge = gestationalAge
        self.ICT_A = NA if ICT_A == NA else ICT_A / MONTHS
        self.ICT_Z = NA if ICT_Z == NA else ICT_Z / MONTHS
        self.preterm = NA

        self.autoICT = NA  # value is set at end of second stage

        self.birthDate = birthDate
        self.birthMonth = birthMonth if birthMonth > 0 else 0
        self.season = season[int(self.birthMonth)]

        # Slope lists:
        # Level1: (height2-height1 / age2-age1)
        # Level2: (height3-height1 / age3-age1) : non-adjacent samples
        self.heightToAgeLevel1 = []
        self.heightToAgeLevel2 = []
        self.heightDivAgeLevel1 = []
        self.heightDivAgeLevel2 = []

        self.weightToAgeLevel1 = []
        self.weightToAgeLevel2 = []
        self.weightDivAgeLevel1 = []
        self.weightDivAgeLevel2 = []

        self.bmiToAgeLevel1 = []
        self.bmiToAgeLevel2 = []
        self.bmiDivAgeLevel1 = []
        self.bmiDivAgeLevel2 = []

        self.max_weightToAgeLevel1 = NA
        self.max_weightToAgeLevel2 = NA
        self.max_weightDivAgeLevel1 = NA
        self.max_weightDivAgeLevel2 = NA
        self.min_weightToAgeLevel1 = NA
        self.min_weightToAgeLevel2 = NA
        self.min_weightDivAgeLevel1 = NA
        self.min_weightDivAgeLevel2 = NA
        self.avg_weightToAgeLevel1 = NA
        self.avg_weightToAgeLevel2 = NA
        self.avg_weightDivAgeLevel1 = NA
        self.avg_weightDivAgeLevel2 = NA
        self.max_heightToAgeLevel1 = NA
        self.max_heightToAgeLevel2 = NA
        self.max_heightDivAgeLevel1 = NA
        self.max_heightDivAgeLevel2 = NA
        self.min_heightToAgeLevel1 = NA
        self.min_heightToAgeLevel2 = NA
        self.min_heightDivAgeLevel1 = NA
        self.min_heightDivAgeLevel2 = NA
        self.avg_heightToAgeLevel1 = NA
        self.avg_heightToAgeLevel2 = NA
        self.avg_heightDivAgeLevel1 = NA
        self.avg_heightDivAgeLevel2 = NA
        self.max_bmiToAgeLevel1 = NA
        self.max_bmiToAgeLevel2 = NA
        self.max_bmiDivAgeLevel1 = NA
        self.max_bmiDivAgeLevel2 = NA
        self.min_bmiToAgeLevel1 = NA
        self.min_bmiToAgeLevel2 = NA
        self.min_bmiDivAgeLevel1 = NA
        self.min_bmiDivAgeLevel2 = NA
        self.avg_bmiToAgeLevel1 = NA
        self.avg_bmiToAgeLevel2 = NA
        self.avg_bmiDivAgeLevel1 = NA
        self.avg_bmiDivAgeLevel2 = NA

        # Stage 2 - formulas which are used to calculate ICT automatically
        self.heightToAgeBurstFormula1 = []
        self.heightToAgeBurstFormula2 = []
        self.heightToAgeBurstFormula3 = []
        self.heightToAgeBurstFormula4 = []

        # Samples:
        self.goodSamples = []
        self.badSamples = []
        self.goodSamplesWithHC = []

    def addSample(self, s, missing=False):  # virtual function
        pass

    def calculateBurst(self):
        goodSamples = sorted([s for s in self.goodSamples if s.age > 0.35])  # don't mind first examples
        for x, y, z in zip(goodSamples, goodSamples[1:], goodSamples[2:]):
            self.heightToAgeBurstFormula1.append((y.age, (z.height / y.height) - (y.height / x.height)))
            self.heightToAgeBurstFormula2.append((y.age, (z.height - y.height) - (y.height - x.height)))
        for x, y, z, w in zip(goodSamples, goodSamples[1:], goodSamples[2:], goodSamples[3:]):
            self.heightToAgeBurstFormula3.append(
                ((y.age + z.age) / 2, ((w.height - y.height) / z.height) - ((z.height - x.height) / y.height)))
        for a, b, c, d, e in zip(goodSamples, goodSamples[1:], goodSamples[2:],
                                              goodSamples[3:], goodSamples[4:]):
            m2 = (e.height - c.height) / (e.age - c.age)
            m1 = (c.height - a.height) / (c.age - a.age)
            midage = (((e.age + c.age) / 2) + ((c.age + a.age) / 2)) / 2
            self.heightToAgeBurstFormula4.append((midage, m2-m1))

    def calculateSlops(self):
        goodSamples = [s for s in self.goodSamples if s.age > 0.35]
        for x, y in zip(goodSamples, goodSamples[1:]):
            if y.age == x.age:
                continue
            self.heightToAgeLevel1.append((y.height - x.height)/(y.age - x.age))
            self.weightToAgeLevel1.append((y.weight - x.weight)/(y.age - x.age))
            self.heightDivAgeLevel1.append((y.height / x.height)/(y.age - x.age))
            self.weightDivAgeLevel1.append((y.weight / x.weight)/(y.age - x.age))
            self.bmiToAgeLevel1.append((y.BMI - x.BMI)/(y.age - x.age))
            self.bmiDivAgeLevel1.append((y.BMI / x.BMI)/(y.age - x.age))
        for x, y in zip(goodSamples, goodSamples[2:]):
            if y.age == x.age:
                continue
            self.heightToAgeLevel2.append((y.height - x.height)/(y.age - x.age))
            self.weightToAgeLevel2.append((y.weight - x.weight)/(y.age - x.age))
            self.heightDivAgeLevel2.append((y.height / x.height)/(y.age - x.age))
            self.weightDivAgeLevel2.append((y.weight / x.weight)/(y.age - x.age))
            self.bmiToAgeLevel2.append((y.BMI - x.BMI)/(y.age - x.age))
            self.bmiDivAgeLevel2.append((y.BMI / x.BMI)/(y.age - x.age))

    def getNumberOfSampls(self, missing=False):
        if not missing:
            return len(self.goodSamples)
        return len(self.badSamples)

    def setPretermFlag(self):
        if self.gestationalAge > NA:
            self.preterm = 1 if self.gestationalAge < 37 else 0
        else:
            self.preterm = NA

    def sortSamplesByAge(self):
        sorted(self.goodSamples)
        sorted(self.badSamples)
        sorted(self.goodSamplesWithHC)

    def generateParametersForRegressionTree(self, first = True):
        pass

    def setValuesOfSlopeVectors(self):
        #### weight slopes ####
        if len(self.weightToAgeLevel1) > 0:
            self.max_weightToAgeLevel1 = max(self.weightToAgeLevel1)
            self.max_weightDivAgeLevel1 = max(self.weightDivAgeLevel1)
            self.min_weightToAgeLevel1 = min(self.weightToAgeLevel1)
            self.min_weightDivAgeLevel1 = min(self.weightDivAgeLevel1)
            self.avg_weightToAgeLevel1 = avg(self.weightToAgeLevel1)
            self.avg_weightDivAgeLevel1 = avg(self.weightDivAgeLevel1)
        if len(self.weightDivAgeLevel2) > 0:
            self.max_weightToAgeLevel2 = max(self.weightToAgeLevel2)
            self.max_weightDivAgeLevel2 = max(self.weightDivAgeLevel2)
            self.min_weightToAgeLevel2 = min(self.weightToAgeLevel2)
            self.min_weightDivAgeLevel2 = min(self.weightDivAgeLevel2)
            self.avg_weightToAgeLevel2 = avg(self.weightToAgeLevel2)
            self.avg_weightDivAgeLevel2 = avg(self.weightDivAgeLevel2)

        #### height slopes ####
        if len(self.heightToAgeLevel1) > 0:
            self.max_heightToAgeLevel1 = max(self.heightToAgeLevel1)
            self.max_heightDivAgeLevel1 = max(self.heightDivAgeLevel1)
            self.min_heightToAgeLevel1 = min(self.heightToAgeLevel1)
            self.min_heightDivAgeLevel1 = min(self.heightDivAgeLevel1)
            self.avg_heightToAgeLevel1 = avg(self.heightToAgeLevel1)
            self.avg_heightDivAgeLevel1 = avg(self.heightDivAgeLevel1)
        if len(self.heightToAgeLevel2) > 0:
            self.avg_heightDivAgeLevel2 = avg(self.heightDivAgeLevel2)
            self.min_heightDivAgeLevel2 = min(self.heightDivAgeLevel2)
            self.max_heightDivAgeLevel2 = max(self.heightDivAgeLevel2)
            self.avg_heightToAgeLevel2 = avg(self.heightToAgeLevel2)
            self.min_heightToAgeLevel2 = min(self.heightToAgeLevel2)
            self.max_heightToAgeLevel2 = max(self.heightToAgeLevel2)

        #### BMI slopes ####
        if len(self.bmiToAgeLevel1) > 0:
            self.max_bmiToAgeLevel1 = max(self.bmiToAgeLevel1)
            self.max_bmiDivAgeLevel1 = max(self.bmiDivAgeLevel1)
            self.min_bmiToAgeLevel1 = min(self.bmiToAgeLevel1)
            self.min_bmiDivAgeLevel1 = min(self.bmiDivAgeLevel1)
            self.avg_bmiToAgeLevel1 = avg(self.bmiToAgeLevel1)
            self.avg_bmiDivAgeLevel1 = avg(self.bmiDivAgeLevel1)
        if len(self.bmiToAgeLevel2) > 0:
            self.min_bmiToAgeLevel2 = min(self.bmiToAgeLevel2)
            self.min_bmiDivAgeLevel2 = min(self.bmiDivAgeLevel2)
            self.avg_bmiToAgeLevel2 = avg(self.bmiToAgeLevel2)
            self.max_bmiDivAgeLevel2 = max(self.bmiDivAgeLevel2)
            self.max_bmiToAgeLevel2 = max(self.bmiToAgeLevel2)
            self.avg_bmiDivAgeLevel2 = avg(self.bmiDivAgeLevel2)

    def __repr__(self):
        return 'Child(id=%s)' % (self.id)

    def __lt__(self, other):
        return self.id < other.id

    def generateParametersForRegressionDecisionTree(self, common_ages, first=True):
        if self.autoICT == NA:
            return [], [], 0
        features = ["sex", "birthWeight (KG)", "birthHeight (M)", "gestationalAge (Weeks)",
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
                "Height at 6 months (m)", "Weight at 6 months (KG)",
                "Height at 6 months (m) Avg'd", "Weight at 6 months (KG) Avg'd",
                "Avg brothers Height at 6 months (m)" , "Avg brothers Weight at 6 months (m)",]
        data = [self.sex, self.birthWeight/KILO, self.birthHeight, self.gestationalAge,
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
            data += [(self.goodSamples[smi]).height,
                     (self.goodSamples[smi]).weight,
                     ((self.goodSamples[smi-1]).height+(self.goodSamples[smi]).height+(self.goodSamples[smi+1]).height) / 3,
                     ((self.goodSamples[smi - 1]).weight + (self.goodSamples[smi]).weight + (self.goodSamples[smi + 1]).weight) / 3]
        b_smi = [find_nearest([a.age for a in x.goodSamples], 0.5) if len(x.goodSamples) else NA for x in self.brothers]
        if NA not in b_smi:
            data += [np.mean([list(self.brothers)[i].goodSamples[b_smi[i]].height for i in range(0, len(b_smi))]),
                     np.mean([list(self.brothers)[i].goodSamples[b_smi[i]].weight for i in range(0, len(b_smi))])]
        else:
            data += [np.nan, np.nan]

        for age in common_ages:
            features += ["Height_at_%s" % str(age), "Weight_at_%s" % str(age), "BMI_at_%s" % str(age)]
            i = find_nearest([a.age for a in self.goodSamples], age)
            if abs(self.goodSamples[i].age - age) > 5 / MONTHS:
                data += [np.nan, np.nan, np.nan]
            else:
                data += [self.goodSamples[i].height, self.goodSamples[i].weight, self.goodSamples[i].BMI]

        return features, data, self.autoICT
