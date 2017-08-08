from Parser.israeliChild import IsraeliChild
import csv
from Parser.auxiliary import *
from datetime import date

def checkMissing(s):
    s = [s[8], s[5], s[6], s[7]] #don't check now HC
    if (s[1] != '' and s[2] != ''):
        s[3] = NA if s[3] == '' else s[3]
        return [float(i) for i in s],False
    return [float(i) if i != '' else NA for i in s], True


def addSamplesToIsraeliChild(headers, sisb, c):
    samples = [s for s in sisb if c.id == (int(s[1]), int(s[2]))]
    for s in samples:  # check valid samples
        s, bool = checkMissing(s)
        c.addSample(s, bool)


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

def addBrothers(children):
    for c in children:
        brothers = [x for x in children if ((c.id)[:-1] == (x.id)[:-1] and x.id!=c.id)]
        for x in brothers:
            c.addBrother(x)

def parseFirstSet():
    israeliChildren = set()
    with open(getpath(ISRAELI_MAIN_FILE), 'r') as f:
        israeliSamples = list(csv.reader(f))
    headers = israeliSamples.pop(0)
    ci = lambda x: float(c[headers.index(x)]) if c[headers.index(x)] != '' else NA
    for c in israeliSamples:
        israeliChildren.add(IsraeliChild((ci('familyN'), ci('indexN')),
                                         getGender(c[headers.index('Sex')]), ci('BirthWeight'),
                                         ci('BirthHeight') / METER if c[headers.index("BirthHeight")] else NA,
                                         ci('GA'), ci('ICT'),
                                         ci('ICT'), ci('indexN'), ci('fatherAge'), ci('motherAge'),
                                         ci('motherWeight'), ci('motherHeight'), '',
                                         ci('birthMonth') if c[headers.index('birthMonth')] != '' else 0))
    addAdditionalInfo(israeliChildren)
    addBrothers(israeliChildren)
    return israeliChildren


def checkMissingSecondSet(s):
    if 0 in s:
        return [float(i) if i != 0 else NA for i in s], True
    return [float(i) for i in s], False


def addAdditionalInfoSecondSetAux(children, file):
    for c in children:
        samples = [[float(s[4])*MONTHS, float(s[6]), float(s[7]), float(s[8])] for s in file if c.id == (int(s[0]), int(s[1]), int(s[2]))]
        for s in samples:
            s, bool = checkMissingSecondSet(s)
            c.addSample(s, bool)
        for s in c.goodSamples:
            if s.age == BIRTH:
                c.height = s.height

def addMotherAge(children, file):
    for c in children:
        samples = [s[9] for s in file if
                   c.id == (int(s[0]), int(s[1]), int(s[2]))]
        mb = set(samples)
        bd = c.birthDate
        if len(mb) > 0:
            mb = mb.pop()
            mb = mb.split('/')  # such as 1,1,2012
            mb.reverse()
            bd = bd.split('/')
            bd.reverse()
            bd = [int(x) for x in bd]
            mb = [int(x) for x in mb]
            ma = (date(bd[0], bd[1], bd[2]) - date(mb[0], mb[1], mb[2])).total_seconds() / 3600 / 24 / 365.25
            c.motherAge = float(format(ma, '.2f'))

def addAdditionalInfoSecondSet(secondSet):
    with open(getpath(ISRAELI_FMLY_RSRCH_FILE), 'r') as f:
        rsrch = list(csv.reader(f))[1:]
        addAdditionalInfoSecondSetAux(secondSet, rsrch)
    with open(getpath(ISRAELI_FMLY_TEST_FILE), 'r') as f:
        test = list(csv.reader(f))[1:]
        addAdditionalInfoSecondSetAux(secondSet, test)
        addMotherAge(secondSet, test)

def addPosition(children):
    for c in children: #only for second
        brothers = [b.id[-1] for b in c.brothers] + [c.id[-1]]
        sorted(brothers)
        c.position = brothers.index(c.id[-1]) + 1

def parseSecondSet():
    with open(getpath(ISRAELI_FMLY_ICT_FILE), 'r') as f:
        israeliSamples = list(csv.reader(f))
    secondSet = set()
    headers = israeliSamples.pop(0)
    ci = lambda x: float(c[headers.index(x)]) if c[headers.index(x)] != '' else NA
    for c in israeliSamples:
        id = tuple((int(x) for x in c[8].split('.')))
        child = IsraeliChild(id, getGender(c[headers.index('Sex')]),
                             ci('BirthWeight'), NA, ci("GA"), ci('ICT'), ci('ICT'),
                             NA, NA, NA, NA, NA, c[5],
                             int(c[5].split('/')[1]))
        secondSet.add(child)
    addAdditionalInfoSecondSet(secondSet)
    addBrothers(secondSet)
    addPosition(secondSet)
    return secondSet


def setMisc(israeliChildren):
    for c in israeliChildren:
        c.setPretermFlag()
        c.calculateSlops()
        c.calculateBurst()
        #c.setValuesOfSlopeVectors()


def parseIsraeli():
    israeliChildren = parseFirstSet()
    secondSet = parseSecondSet()
    israeliChildren = israeliChildren.union(secondSet)
    setMisc(israeliChildren)
    return israeliChildren
