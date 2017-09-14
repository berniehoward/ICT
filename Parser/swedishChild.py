from Parser.child import Child
from Parser.sample import SwedishSample
from Parser.auxiliary import NA, METER, KILO, Nationality

class SwedishChild(Child):

    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z, birthDate, birthMonth):

        Child.__init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z,
                       birthDate, birthMonth)
        self.birthWeight = self.birthWeight * KILO
        self.mHeight = NA
        self.fHeight = NA

    def addSample(self, s, missing=False):
        sample = SwedishSample(s[1], s[2], s[3])
        if not missing:
            self.goodSamples.append(sample)
        else:
            self.badSamples.append(sample)

    def setParentHeights(self, l):
        self.mHeight = float(l[1]) / METER if l[1] != '' else NA
        self.fHeight = float(l[2]) / METER if l[2] != '' else NA

    def __repr__(self):
        return 'SwedishChild(id=%s)' % (self.id)

    def generateParametersForRegressionDecisionTree(self, common_ages, first=True):
        features, data, c = super(SwedishChild, self).generateParametersForRegressionDecisionTree(common_ages, first)

        features += ["fatherHeight (M)", "motherHeight (M)"]
        data += [self.fHeight, self.mHeight]

        features, data = self.generateWHOparameters(common_ages, features, data)

        features += ["nation"]
        data += [Nationality.SWE.value]

        if self.autoICT == NA:
            return features, data, 0

        return features, data, self.autoICT

    def generateWHOparameters(self, common_ages, features, data):
        features, data = super(SwedishChild, self).generateWHOparameters(common_ages, features, data)
        return features, data