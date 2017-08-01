import csv
from operator import itemgetter
from Parser.swedishChild import SwedishChild
from Parser.auxiliary import *

# Formats the dataset for further usage (floats etc)
def formatFirstSwedishDataset(samples):
    s = []
    for sample in samples:
        sample[5] = NA if sample[5] == 'NA' else sample[5]
        sample[6] = NA if sample[6] == 'NA' else sample[6]
        sample[4] = getGender(sample[4])
        s.append([float(cell) if cell != '' else cell for cell in sample])
    return s

BIRTH = 0
checkMissing = lambda s: False if all([s[1], s[2], s[3]]) else True #bool value to check missing values

# Creates a child with good and bad samples
def createSwedishChildrenWithSamples(samples, ids):
    swedishChildren = set()
    for id in ids:  # id = tup(id,ictA,ictZ,GA)
        (ictA, ictZ, GA) = (id[1], id[2], id[3])
        samplesForId = sorted([s for s in samples if s[0] == id[0]],key=itemgetter(1))
        for s in samplesForId:
            if(s[1] == BIRTH): #work around for bad birth records
                (s[7], s[8], s[9]) = (s[2], s[3], GA)
                swedishChild = SwedishChild(s[0], s[4], s[2], s[3], s[9], s[5], s[6], NA, NA)
                swedishChildren.add(swedishChild)
            s[5], s[6] = (ictA, ictZ)
            swedishChild.addSample(s, checkMissing(s))
    return swedishChildren

# Parse first given file
def praseFirstSwedish():
    with open(getpath(SWEDISH_FILE), 'r') as f:
        swedishSamples = list(csv.reader(f))
    swedishSamples = formatFirstSwedishDataset(swedishSamples[1:])
    idsWithICT = [[sample[0], sample[5], sample[6]] for sample in swedishSamples if sample[5] != '' or sample[6] != '']
    idandGA = [[sample[0], sample[9]] for sample in swedishSamples if sample[9] != '']
    for i in idsWithICT:  # merge GA with other data, workaround because of stupid dataset
        for j in idandGA:
            if i[0] == j[0]:
                i.append(j[1])
                break
        i.append(NA)
    return createSwedishChildrenWithSamples(swedishSamples, idsWithICT)

def addLatterSamplesToChild(c, samples):
    samplesForId = sorted([s for s in samples if float(s[0]) == c.id])
    for s in samplesForId:
        mod_s = [float(s[0]), float(s[9]), float(s[5]) if s[5] != '' else '', float(s[4]) if s[4] != '' else '']
        c.addSample(mod_s, checkMissing(mod_s))

def manageLatterSampleSets(children, samples, str):
    for s in samples:
        if float(s[9]) == BIRTH:
            mod_s = [s[0], s[6], s[5], s[4], s[2], s[1], s[1], float(s[8].split('/')[1])]
            mod_s = [float(field) if field else NA for field in mod_s]
            sc = SwedishChild(mod_s[0], mod_s[1], mod_s[2], mod_s[3], mod_s[4], mod_s[5], mod_s[6], s[8], mod_s[7])
            sp = ''
            if (str == "Boys"):
                with open(getpath(SWEDISH_NEW_BOYS_P_FILE), 'r') as f:
                    sp = list(csv.reader(f))[1:]
            else:
                with open(getpath(SWEDISH_NEW_GIRLS_P_FILE), 'r') as f:
                    sp = list(csv.reader(f))[1:]
            for i in [s for s in sp if s[0] == sc.id]:
                sc.setParentHeights(i)
            children.add(sc)
            addLatterSamplesToChild(sc, samples)

def praseSecondSwedish(swedishChildren):
    with open(getpath(SWEDISH_NEW_BOYS_FILE), 'r') as f:
        swedishBoysSamples = list(csv.reader(f))
    manageLatterSampleSets(swedishChildren, swedishBoysSamples[1:], "Boys")
    with open(getpath(SWEDISH_NEW_GIRLS_FILE), 'r') as g:
        swedishGirlsSamples = list(csv.reader(g))
    manageLatterSampleSets(swedishChildren, swedishGirlsSamples[1:], "Girls")

def setMisc(swedishChildren):
    for c in swedishChildren:
        c.setPretermFlag()
        c.calculateSlops()
        c.calculateBurst()

# Swedish child pareser main function
def parseSwedish():
    swedishChildren = praseFirstSwedish()
    print("OK")
    praseSecondSwedish(swedishChildren)
    setMisc(swedishChildren)
    return swedishChildren