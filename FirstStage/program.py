from Parser.auxiliary import MONTHS
from FirstStage.firstStageFunc import *
from scipy import stats


def program(dictionary):
    for c in dictionary.swedishChildren:
        print(len(c.goodSamples))
    heights, children = findHeightAroundAge(list(dictionary.swedishChildren))
    normalizedHeights = stats.zscore(heights)
    h1, h2, h3, h4, h5, h_na = divideToGroups(normalizedHeights, children, -1, -0.5, 0.5, 1)
    epsilons = [0.04, 0.05, 0.06, 0.07]
    for e in epsilons:
        icts = [findICTByEpsilon(e, c) for c in children]
        g1, g2, g3, g4, g5, g_na = divideToGroups(icts, children, 7/MONTHS, 8.5/MONTHS, 9.5/MONTHS, 10.5/MONTHS)
        print(len(g1), len(g2), len(g3), len(g4), len(g5), len(g_na))




