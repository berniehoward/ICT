from child import Child
from sample import SwedishSample

class SwedishChild(Child):

    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z):
        Child.__init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z)

    def addSample(self, s, missing = False):
        sample = SwedishSample(s[1], s[2], s[3])
        if missing == False:
            self.goodSamples.append(sample)
        else:
            self.badSamples.append(sample)
