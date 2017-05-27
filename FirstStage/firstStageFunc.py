from Utility import find_nearest
from Parser.auxiliary import NA
from scipy import stats
from scipy import append as npappend
from itertools import chain

FIRST_AGE = 0.5
RANGE = 0.3

cs = lambda c, idx, n,r : abs(c.goodSamples[idx].age - n) < r

def calcScore(s_6_heights, f_6_heights, children6, s_7_heights, f_7_heights, children7):
    normalized_f6_heights = stats.zscore(f_6_heights)
    normalized_f7_heights = stats.zscore(f_7_heights)
    normalized_s6_heights = stats.zscore(s_6_heights)
    normalized_s7_heights = stats.zscore(s_7_heights)
    heights6 = normalized_s6_heights - normalized_f6_heights
    heights7 = normalized_s7_heights - normalized_f7_heights
    return list(chain(heights6, heights7)), list(chain(children6, children7))

def findHeightAroundAge(listOfChildren):
    f_6_heights = []
    f_7_heights = []
    s_6_heights = []
    s_7_heights = []
    children6 = []
    children7 = []
    for child in listOfChildren:
        child.calculateBurst() #on the fly
        f_idx = find_nearest([a.age for a in child.goodSamples], FIRST_AGE)
        s_6_idx = find_nearest([a.age for a in child.goodSamples], 6)
        s_7_idx = find_nearest([a.age for a in child.goodSamples], 7)

        if abs(child.goodSamples[f_idx].age - FIRST_AGE) < 0.1 and \
            (abs(child.goodSamples[s_7_idx].age - 7) < RANGE):
            print(child.goodSamples[f_idx].age, child.goodSamples[s_7_idx].age)
            f_7_heights.append(child.goodSamples[f_idx].height)
            s_7_heights.append(child.goodSamples[s_7_idx].height)
            children7.append(child)
        if abs(child.goodSamples[f_idx].age - FIRST_AGE) < RANGE/2 and \
            (abs(child.goodSamples[s_6_idx].age - 6) < RANGE):
            print(child.goodSamples[f_idx].age, child.goodSamples[s_6_idx].age)
            f_6_heights.append(child.goodSamples[f_idx].height)
            s_6_heights.append(child.goodSamples[s_6_idx].height)
            children6.append(child)

    return calcScore(s_6_heights, f_6_heights, children6, s_7_heights, f_7_heights, children7)
    #print("normalized_f_heights", stats.mstats.normaltest(f_heights))
    #print("normalized_s_heights", stats.mstats.normaltest(s_heights))


def divideToGroups(featureList, children, b1, b2, b3):
    g1 = []
    g2 = []
    g3 = []
    g4 = []
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
        else:
            g4.append(c)
    return g1, g2, g3, g4, g_na


def findICTByEpsilon(e,child):
    for midAge, slope in child.heightToAgeBurst:
        if slope > e:
            return midAge
    return NA

