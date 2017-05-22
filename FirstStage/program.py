from Parser.auxiliary import MONTHS
from FirstStage.firstStageFunc import *
from scipy import stats


def program(dictionary):
    heights, children = findHeightAroundAge(list(dictionary.swedishChildren))
    normalizedHeights = stats.zscore(heights)
    h1, h2, h3, h4, h5, h_na = divideToGroups(normalizedHeights, children, -0.7, -0.2, 0.3, 0.7)
    epsilons = [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    for e in epsilons:
        icts = [findICTByEpsilon(e, c) for c in children]
        g1, g2, g3, g4, g5, g_na = divideToGroups(icts, children, 5/MONTHS, 9/MONTHS, 13/MONTHS, 17/MONTHS)
        print(len(g1), len(g2), len(g3), len(g4), len(g5), len(g_na))

        """ 65 14 11 3 5 0
            46 12 21 6 13 0
            31 8 24 6 29 1
            23 4 31 6 34 4
            25 3 30 4 36 11
            25 3 27 2 41 15
            23 2 24 2 47 19"""




