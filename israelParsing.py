getpath = lambda file: os.path.join(os.getcwd(),"ICTData",file)
from time import strptime
from israeliChild import IsraeliChild
from operator import itemgetter
import sys,os, csv, math
from auxiliary import *
import dateutil.parser as dateParser

#familyN    FMN	indexN	ICT	Sex	ageMother	ageFather	WeightMother	heightMother	monthBirth	GestationalAge	BirthWeight	BirthHeight	HeadCirc

"""self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z, \
                 birthPosition, fatherAge, motherAge, motherWeight, motherHeight, \
                 birthMonth, birthYear"""

def addAdditionalInfo(israeliChildren):
    with open(getpath(ISRAELI_ADDITIONAL_INFO_FILE), 'r') as f:
        sisb = list(csv.reader(f))
        headers = sisb.pop(0)
        for c in israeliChildren:
            date = lambda x: x[headers.index('birthDate')]
            ci = lambda l, x: float(l[headers.index(x)])
            f, i = c.id
            print(f,i)
            datelist = [date(x) for x in sisb if (ci(x,'familyN') == f and (ci(x,'indexN')==i))]
            birthDate = datelist[0] if len(datelist)>0 else FALSE_DATE
            c.updateYear(int(birthDate.split('/')[2]))
    #TODO: add samples

def parseIsraeli():
    israeliChildren = set()
    with open(getpath(ISRAELI_MAIN_FILE), 'r') as f:
        israeliSamples = list(csv.reader(f))
    headers = israeliSamples.pop(0)
    for c in israeliSamples:
        ci = lambda x: float(c[headers.index(x)]) if c[headers.index(x)] != '' else NA
        print(headers)
        print(ci('familyN'),ci('indexN'), ci('birthMonth') if c[headers.index('birthMonth')] != '' else 0)
        israeliChildren.add(IsraeliChild((ci('familyN'),ci('indexN')),
            getGender(c[headers.index('Sex')]), ci('BirthWeight'),
            ci('BirthHeight')/METER,
            ci('GA'), ci('ICT'),
            NA, ci('indexN'), ci('fatherAge'), ci('motherAge'),
            ci('motherWeight'),
            ci('motherHeight'),
            ci('birthMonth') if c[headers.index('birthMonth')] != '' else 0))
    addAdditionalInfo(israeliChildren)