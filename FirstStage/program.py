from Parser.auxiliary import MONTHS
from FirstStage.firstStageFunc import *
from scipy import stats
from simpleai import search

def ictHeightCorrelation(epsilons, children):
    for e in epsilons:
        icts = [findICTByEpsilon(e, c) for c in children]
        #print(icts)
        g1, g2, g3, g4, g_na = divideToGroups(icts, children, 5/MONTHS, 10/MONTHS, 15/MONTHS)
        print(len(g1),len(g2), len(g3), len(g4))


def program(dictionary):
    heights, children = findHeightAroundAge(list(dictionary.swedishChildren))
    print(len(children))
    h1, h2, h3, h4, h_na = divideToGroups(heights, children, -2, 0, 2)
    for i in [h1,h2,h3,h4]:
        print([c.id for c in i])
    RESTARTS = 10
    #search.local.hill_climbing_random_restarts(,RESTARTS)
    epsilons = [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    ictHeightCorrelation(epsilons, children)

