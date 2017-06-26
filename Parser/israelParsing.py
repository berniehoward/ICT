from Parser.israeliChild import IsraeliChild
import csv
from Parser.auxiliary import *

def checkMissing(s):
    s = [s[8], s[5], s[6], s[7]]
    if all(s):
        return ([float(i) for i in s],False)
    return ([float(i) if i != '' else NA for i in s],True)

def addSamplesToIsraeliChild(headers, sisb, c):
    samples = [s for s in sisb if c.id == (int(s[1]),int(s[2]))]
    for s in samples: #check valid samples
        s,bool = checkMissing(s)
        c.addSample(s,bool)


def addAdditionalInfo(israeliChildren):
    with open(getpath(ISRAELI_ADDITIONAL_INFO_FILE), 'r') as f:
        sisb = list(csv.reader(f))
        headers = sisb.pop(0)
        for c in israeliChildren:
            date = lambda x: x[headers.index('birthDate')]
            ci = lambda l, x: float(l[headers.index(x)])
            f, i = c.id
            datelist = [date(x) for x in sisb if (ci(x,'familyN') == f and (ci(x,'indexN')==i))]
            birthDate = datelist[0] if len(datelist)>0 else FALSE_DATE
            c.updateYear(int(birthDate.split('/')[2]))
            addSamplesToIsraeliChild(headers, sisb, c)
            c.calculateSlops()
            c.calculateBurst()

def parseIsraeli():
    israeliChildren = set()
    with open(getpath(ISRAELI_MAIN_FILE), 'r') as f:
        israeliSamples = list(csv.reader(f))
    headers = israeliSamples.pop(0)
    for c in israeliSamples:
        ci = lambda x: float(c[headers.index(x)]) if c[headers.index(x)] != '' else NA
        israeliChildren.add(IsraeliChild((ci('familyN'),ci('indexN')),
            getGender(c[headers.index('Sex')]), ci('BirthWeight'),
            ci('BirthHeight')/METER if c[headers.index("BirthHeight")] else NA,
            ci('GA'), ci('ICT'),
            NA, ci('indexN'), ci('fatherAge'), ci('motherAge'),
            ci('motherWeight'),
            ci('motherHeight'),
            ci('birthMonth') if c[headers.index('birthMonth')] != '' else 0))
    addAdditionalInfo(israeliChildren)
    print([(x, x.goodSamples, x.badSamples) for x in israeliChildren if x.id == (101.0, 5.0)])
    return israeliChildren