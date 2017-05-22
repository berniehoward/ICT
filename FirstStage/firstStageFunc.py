from Utility import find_nearest
from Parser.auxiliary import NA

AGE = 6.5
RANGE = 1.0

def findHeightAroundAge(listOfChildren):
    heights = []
    children = []
    for child in listOfChildren:
        child.calculateBurst() #on the fly
        idx = find_nearest([a.age for a in child.goodSamples], AGE)
        if abs(child.goodSamples[idx].age - AGE) < RANGE:
            heights.append(child.goodSamples[idx].height)
            children.append(child)
    return heights, children


def divideToGroups(featureList, children, b1, b2, b3, b4):
    g1 = []
    g2 = []
    g3 = []
    g4 = []
    g5 = []
    g_na = []
    for f, c in zip(featureList, children):
        if f == NA:
            g_na.append(c)
        if f < b1:
            g1.append(c)
        elif b1 <= f <= b2:
            g2.append(c)
        elif b2 <= f <= b3:
            g3.append(c)
        elif b3 <= f <= b4:
            g4.append(c)
        else:
            g5.append(c)
    return g1, g2, g3, g4, g5, g_na


def findICTByEpsilon(e,child):
    for midAge, slope in child.heightToAgeBurst:
        if slope > e:
            return midAge
    return NA

