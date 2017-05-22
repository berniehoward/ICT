from Parser.auxiliary import MONTHS
from FirstStage.firstStageFunc import *
from scipy import stats


def program(dictionary):
    heights, children = findHeightAroundAge(list(dictionary.swedishChildren))
    normalizedHeights = stats.zscore(heights)
    g1, g2, g3, g_na = divideToGroups(normalizedHeights, children, -0.5, 0.5)
    epsilons = [0.005]
    for e in epsilons:
        icts = [findICTByEpsilon(e, c) for c in children]
        g1, g2, g3, g_na = divideToGroups(icts, children, 8/MONTHS, 12/MONTHS)
        print(len(g1), len(g2), len(g3), len(g_na))




