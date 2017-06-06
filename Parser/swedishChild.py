from Parser.child import Child

from Parser.sample import SwedishSample


class SwedishChild(Child):

    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z):
        Child.__init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z)

    def addSample(self, s, missing=False):
        sample = SwedishSample(s[1], s[2], s[3])
        if not missing:
            self.goodSamples.append(sample)
        else:
            self.badSamples.append(sample)

    def __repr__(self):
        return 'SwedishChild(id=%s)' % (self.id)