from Parser.child import Child
from Parser.sample import SwedishSample
from Parser.auxiliary import NA, METER

class SwedishChild(Child):

    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z, birthDate, birthMonth):

        Child.__init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z,
                       birthDate, birthMonth)

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
        self.mHeight = float(l[2]) / METER if l[2] != '' else NA

    def __repr__(self):
        return 'SwedishChild(id=%s)' % (self.id)