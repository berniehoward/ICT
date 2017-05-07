


class childrenDictionary():

    def __init__(self):
        self.swedishChildren = set()
        self.israeliChildren = set()

    def addSwedish(self, c):
        self.swedishChildren.add(c)

    def addIsraeli(self, c):
        self.swedishChildren.add(c)

    def getSamplesCount(self):
        lenGoodS = len([c.goodSamples for c in self.swedishChildren])
        lenBadS = len([c.badSamples for c in self.swedishChildren])
        lenGoodI = len([c.goodSamples for c in self.israeliChildren])
        lenBadI = len([c.badSamples for c in self.israeliChildren])
        return lenGoodS, lenGoodI, lenBadS, lenBadI

    def getNumOfchildren(self, type):
        if type == "S":
            return len(self.swedishChildren)
        return len(self.israeliChildren)

    def getNumOfSwedishSampls(self, missing = False):
        # return (avg, min, max, hist)
        max_s = 0
        sum_s = 0
        min_s = 400000
        hist = [0] * 45
        numOfChildren = len(self.swedishChildren)
        for c in self.swedishChildren:
            sampls = c.getNumberOfSampls(missing)
            if max_s < sampls:
                max_s = sampls
            if min_s > sampls:
                min_s = sampls
            sum_s += sampls
            hist[sampls] += 1
        return sum_s/numOfChildren, min_s, max_s, hist
