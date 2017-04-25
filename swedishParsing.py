from swedishChild import SwedishChild
from operator import itemgetter
import csv
from auxiliary import *

def formatSwedishDataset(samples):
    s = []
    for sample in samples:
        sample[5] = NA if sample[5] == 'NA' else sample[5]
        sample[6] = NA if sample[6] == 'NA' else sample[6]
        sample[4] = getGender(sample[4])
        s.append([float(cell) if cell != '' else cell for cell in sample])
    return s

BIRTH = 0
checkMissing = lambda s: True if '' in s else False

def createSwedishChildrenAndSamples(samples, ids):
    swedishChildren = set()
    for id in ids: #id = tup(id,ictA,ictZ,GA)
        (ictA,ictZ,GA) = (id[1],id[2],id[3])
        samplesForId = sorted([s for s in samples if s[0] == id[0]],key=itemgetter(1))
        for s in samplesForId:
            if(s[1] == BIRTH):
                (s[7], s[8], s[9]) = (s[2], s[3], GA)
                swedishChild = SwedishChild(s[0], s[4], s[2], s[3], s[9], s[5], s[6])
                swedishChildren.add(swedishChild)
            s[5],s[6] = (ictA, ictZ)
            swedishChild.addSample(s, checkMissing(s))
        swedishChild.calculateSlops()
        print(swedishChild.id, swedishChild.heightToAgeLevel1)
    return swedishChildren

def parseSwedish():
    with open(getpath(SWEDISH_FILE), 'r') as f:
        swedishSamples = list(csv.reader(f))
    headers = swedishSamples.pop(0)
    swedishSamples = formatSwedishDataset(swedishSamples)
    idsWithICT = [[sample[0],sample[5],sample[6]] for sample in swedishSamples if sample[5] != '' or sample[6] != '']
    idandGA = [[sample[0],sample[9]] for sample in swedishSamples if sample[9] !='']
    for i in idsWithICT: #yuck
        for j in idandGA:
            if (i[0] - j[0] < 0.01):
                i.append(j[1])
                break
    #print(idsWithICT)
    return createSwedishChildrenAndSamples(swedishSamples, idsWithICT)
