from Parser.auxiliary import *
from operator import attrgetter

season = [NA, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 0, 0]  # winter, spring, summer, fall


class Child:
    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z,
                 birthDate, birthMonth):

        # General info:
        self.id = id
        self.sex = sex
        self.birthWeight = birthWeight
        self.birthHeight = birthHeight
        self.gestationalAge = gestationalAge
        self.ICT_A = NA if ICT_A == NA else ICT_A / MONTHS
        self.ICT_Z = NA if ICT_Z == NA else ICT_Z / MONTHS

        self.preterm = NA

        self.birthDate = birthDate
        self.birthMonth = birthMonth if birthMonth > 0 else 0
        self.season = season[int(self.birthMonth)]

        # ICT info:
        if ICT_A == NA and ICT_Z == NA:
            self.ICT_AVG = NA
        elif ICT_A == NA or ICT_Z == NA:
            self.ICT_AVG = self.ICT_Z if self.ICT_A == NA else self.ICT_A
        else:
            self.ICT_AVG = (self.ICT_A + self.ICT_Z) / 2

        self.ICT_MIN = min(self.ICT_A, self.ICT_Z)
        self.ICT_MAX = max(self.ICT_A, self.ICT_Z)

        # Slope lists:
        # Level1: (height1-height2 / age1-age2)
        # Level2: (height1-height3 / age1-age3) : non-adjacent samples
        self.heightToAgeLevel1 = []
        self.heightToAgeLevel2 = []
        self.weightToAgeLevel1 = []
        self.weightToAgeLevel2 = []
        self.bmiToAgeLevel1 = []
        self.bmiToAgeLevel2 = []

        # Stage 2 - formulas which are used to calculate ICT automatically
        self.heightToAgeBurstFormula1 = []
        self.heightToAgeBurstFormula2 = []
        self.heightToAgeBurstFormula3 = []
        self.heightToAgeBurstFormula4 = []

        # Samples:
        self.goodSamples = []
        self.badSamples = []

    def __repr__(self):
        return 'Child(id=%s)' % (self.id)

    def addSample(self, s, missing=False):  # virtual function
        pass

    def calculateBurst(self):
        goodSamples = sorted([s for s in self.goodSamples if s.age > 0.35])  # don't mind first examples
        for x, y, z in zip(goodSamples, goodSamples[1:], goodSamples[2:]):
            self.heightToAgeBurstFormula1.append((y.age, (z.height / y.height) - (y.height / x.height)))
            self.heightToAgeBurstFormula2.append((y.age, (z.height - y.height) - (y.height - x.height)))
            m = (z.height - x.height) / (z.age - x.age)
            self.heightToAgeBurstFormula4.append((y.age, m))
        for x, y, z, w in zip(goodSamples, goodSamples[1:], goodSamples[2:], goodSamples[3:]):
            self.heightToAgeBurstFormula3.append(
                ((y.age + z.age) / 2, ((w.height - y.height) / z.height) - ((z.height - x.height) / y.height)))

        # dividedSamples = [goodSamples[i:i + 3] for i in range(0, len(goodSamples), 3)]
        # dividedSamples = [x for x in dividedSamples if len(x) == 3]
        # for (x1, y1, z1), (x2, y2, z2) in zip(dividedSamples, dividedSamples[1:]):
        #     #print((x1, y1, z1), (x2, y2, z2))
        #     m1 = (z1.height - x1.height) / (z1.age - x1.age)
        #     m2 = (z2.height - x2.height) / (z2.age - x2.age)
        #     print(m2-m1)
        #     midage = (((z2.age + x2.age) / 2) + ((z1.age + x1.age) / 2)) / 2
        #     self.heightToAgeBurstFormula4.append((midage, m2 - m1))
        # print()

    def calculateSlops(self):
        goodSamples = [s for s in self.goodSamples if s.age > 0.35]
        for x, y in zip(goodSamples, goodSamples[1:]):
            self.heightToAgeLevel1.append(y.height - x.height)
            self.weightToAgeLevel1.append(y.weight - x.weight)
            self.bmiToAgeLevel1.append(y.BMI - x.BMI)
        for x, y in zip(goodSamples, goodSamples[2:]):
            self.heightToAgeLevel2.append(y.height - x.height)
            self.weightToAgeLevel2.append(y.weight - x.weight)
            self.bmiToAgeLevel2.append(y.BMI - x.BMI)

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

    def __lt__(self, other):
        return self.id < other.id
