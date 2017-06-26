import csv
from operator import itemgetter

from Parser.swedishChild import SwedishChild

from Parser.auxiliary import *

# Formats the dataset for further usage (floats etc)
def formatSwedishDataset(samples):
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
                swedishChild = SwedishChild(s[0], s[4], s[2], s[3], s[9], s[5], s[6])
                swedishChildren.add(swedishChild)
            s[5], s[6] = (ictA, ictZ)
            swedishChild.addSample(s, checkMissing(s))
        swedishChild.calculateSlops()
        swedishChild.calculateBurst()
    return swedishChildren

# Parse first given file
def praseFirstSwedish():
    with open(getpath(SWEDISH_FILE), 'r') as f:
        swedishSamples = list(csv.reader(f))
    swedishSamples = formatSwedishDataset(swedishSamples[1:])
    idsWithICT = [[sample[0], sample[5], sample[6]] for sample in swedishSamples if sample[5] != '' or sample[6] != '']
    idandGA = [[sample[0], sample[9]] for sample in swedishSamples if sample[9] != '']
    for i in idsWithICT:  # merge GA with other data, workaround because of stupid dataset
        for j in idandGA:
            if i[0] == j[0]:
                i.append(j[1])
                break
        i.append(NA)
    return createSwedishChildrenWithSamples(swedishSamples, idsWithICT)

def manageLaterSamplesSets(samples):
    for s in samples:
        # ID,Mesurement_date,ICT_months,GA_weeks,Birth_date,
        # G_age_years,Height_cm,Weight_kg,GenderB1G2,MdateSAS,BdateSAS,diff
        sample_age = s[11]
        if sample_age == BIRTH:
            pass# swedishChildren.add()


def praseSecondSwedish(swedishChildren):
    with open(getpath(SWEDISH_NEW_BOYS_FILE), 'r') as f:
        swedishBoysSamples = list(csv.reader(f))
    with open(getpath(SWEDISH_NEW_GIRLS_FILE), 'r') as g:
        swedishGirlsSamples = list(csv.reader(g))
        manageLaterSamplesSets(swedishChildren, swedishBoysSamples[1:])
        manageLaterSamplesSets(swedishChildren, swedishGirlsSamples[1:])

# Swedish child pareser main function
def parseSwedish():
    swedishChildren = praseFirstSwedish()
    praseSecondSwedish(swedishChildren)