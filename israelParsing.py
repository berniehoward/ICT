getpath = lambda file: os.path.join(os.getcwd(),"ICTData",file)
from time import strptime
from israeliChild import IsraeliChild
from operator import itemgetter
import sys,os, csv, math
from auxiliary import *

#familyN    FMN	indexN	ICT	Sex	ageMother	ageFather	WeightMother	heightMother	monthBirth	GestationalAge	BirthWeight	BirthHeight	HeadCirc

"""self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z, \
                 birthPosition, fatherAge, motherAge, motherWeight, motherHeight, \
                 birthMonth, birthYear"""

def getBirthYear(child):


def crossWithSISB(israeliSamples):
    ci = lambda x: c.index(x)
    headers = israeliSamples.pop(0)
    for c in israeliSamples:
        child = IsraeliChild((ci('familyN'),ci('indexN')), getGender(ci('Sex')),
            ci('BirthWeight')/KILO, ci('BirthHeight')/METER, ci('GA'), ci('ICT'),
            NA, ci('indexN'), ci('fatherAge'), ci('motherAge'), ci('motherWeight'),
            ci('motherHeight'), ci('birthMonth'), getBirthYear(child))

def parseIsraeli():
    with open(getpath(ISRAELI_MAIN_FILE), 'r') as f:
        israeliSamples = crossWithSISB((list(csv.reader(f))))