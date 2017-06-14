from math import ceil
from Parser.auxiliary import *

BMI = lambda w,h: w/h**2

class Sample:
    def __init__(self, age, weight, height):
        self.age = float(format(age, '.2f'))
        self.weight = weight
        if weight == '' or height == '':
            self.height = NA
            self.BMI = NA
        else:
            self.height = height / METER
            self.BMI = BMI(self.weight, self.height)

    def __repr__(self):
        return 'Sample(Age=%s,Height=%s)' % (self.age,self.height)

class SwedishSample(Sample):
    def __init__(self, age, weight, height):
        Sample.__init__(self, age, weight, height)

    def __repr__(self):
        return 'SwedishSample(Age=%s,Height=%s)' % (self.age,self.height)

class IsraeliSample(Sample):
    def __init__(self, age, weight, height, HC):
        Sample.__init__(self, age, weight, height)

        self.HC = HC
        self.HCdivHeight = HC/height
        self.HCdivHeightSq = HC / height**2
        self.HCdivWeight = HC/weight
        self.HCdivWeightSq = HC / weight**2

    def __repr__(self):
        return 'IsraeliSample(Age=%s,Height=%s)' % (self.age,self.height)