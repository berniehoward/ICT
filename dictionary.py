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