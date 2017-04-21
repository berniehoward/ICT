from child import Child

season = [0,1,1,1,2,2,2,3,3,3,0,0] #winter, spring, summer, fall
class IsraeliChild(Child):

    def __init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z, \
                 familyID, birthPosition, fatherAge, motherAge, motherWeight, motherHeight, \
                 birthMonth, birthYear):

        Child.__init__(self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z)

        #family related information
        self.familyID = familyID
        self.position = birthPosition
        self.fatherAge = fatherAge
        self.motherAge = motherAge
        self.motherWeight = motherWeight
        self.motherHeight = motherHeight
        self.brothers = set()

        self.birthYear = birthYear
        self.birthMonth = birthMonth
        self.season = season[birthMonth]

    def addBrother(self, brother):
        self.brothers.add(brother)



