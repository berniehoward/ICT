from math import ceil
from Parser.auxiliary import *

BMI = lambda w,h: w/h**2

class Sample:
    def __init__(self, age, weight, height):
        self.age = float(format(age, '.2f'))
        self.weight = weight
        if weight == '' or height == '' or weight == 0 or height == 0:
            self.height = NA
            self.BMI = NA
        else:
            self.height = height / METER if height != NA else NA
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
        Sample.__init__(self, age/MONTHS, weight, height)

        self.HC = HC

        if HC > 0 and weight > 0 and height > 0:
            self.HCdivHeight = HC/height
            self.HCdivHeightSq = HC / height**2
            self.HCdivWeight = HC/weight
            self.HCdivWeightSq = HC / weight**2
        else:
            self.HC = NA
            self.HCdivHeight = NA
            self.HCdivHeightSq = NA
            self.HCdivWeight = NA
            self.HCdivWeightSq = NA

    def __repr__(self):
        return 'IsraeliSample(Age=%s,Height=%s)' % (self.age,self.height)