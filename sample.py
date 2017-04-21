BMI = lambda w,h: w/h**2

class Sample:
    def __init__(self, age, weight, height):
        self.age = age
        self.weight = weight
        self.height = height
        self.BMI = BMI(weight,height)

class isreliSample(Sample):
    def __init__(self, age, weight, height, HC):
        Sample.__init__(self, age, weight, height)

        self.HC = HC
        self.HCdivHeight = HC/height
        self.HCdivHeightSq = HC / height**2
        self.HCdivWeight = HC/weight
        self.HCdivWeightSq = HC / weight**2
