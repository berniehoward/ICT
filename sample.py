from constants import *
from math import ceil

BMI = lambda w,h: w/h**2

class Sample:
    def __init__(self, age, weight, height):
        self.age = ceil(365*age)
        self.weight = weight
        if weight == '' or height == '':
            self.height = -100
            self.BMI = NA
        else:
            self.height = height / METER
            self.BMI = BMI(self.weight, self.height)
            print(self.weight, self.height, self.BMI)

class isreliSample(Sample):
    def __init__(self, age, weight, height, HC):
        Sample.__init__(self, age, weight, height)

        self.HC = HC
        self.HCdivHeight = HC/height
        self.HCdivHeightSq = HC / height**2
        self.HCdivWeight = HC/weight
        self.HCdivWeightSq = HC / weight**2
