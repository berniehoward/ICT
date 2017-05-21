from Utility import find_nearest
from Parser.auxiliary import NA

AGE = 6.5
RANGE = 1.0



def findHeightAroundAge(listOfChildren):
    heights = []
    children = []
    for child in listOfChildren:
        child.calculateBurst()
        idx = find_nearest([a.age for a in child.goodSamples], AGE)
        if abs(child.goodSamples[idx].age - AGE) < RANGE:
            heights.append(child.goodSamples[idx].height)
            children.append(child)
    return heights, children


def divideToGroups(featureList, children, low_border, high_border):
    g1 = []
    g2 = []
    g3 = []
    g_out = []
    for f, c in zip(featureList, children):
        if f == NA:
            g_out.append(c)
        if f < low_border:
            g1.append(c)
        elif low_border <= f <= high_border:
            g2.append(c)
        else:
            g3.append(c)
    return g1, g2, g3, g_out


def findICTByEpsilon(e,child):
    for midAge, slope in child.heightToAgeBurst:
        if slope > e:
            return midAge
    return NA

