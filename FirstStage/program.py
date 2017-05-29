from Parser.auxiliary import MONTHS
from FirstStage.firstStageFunc import *
from scipy import stats
from simpleai import search
import operator

def findChildGroup(c, heights):
    for g in heights:
        if c in g and heights.index(g):
            return heights.index(g)
    return NA

def scoreEpsilonByManhattanDistances(dbe, heights): #score epsilon values using manhathan distances
    sum = 0
    for g in dbe: #group in dividedByEpsilon
        for c in g:
            print(c.id, dbe.index(g), findChildGroup(c,heights))
            sum += abs(dbe.index(g) - findChildGroup(c,heights))
    #print(sum)
    return sum

def ictHeightCorrelation(epsilons, children, heights):
    m = (NA, NA)
    for e in epsilons:
        icts = [findICTByEpsilon(e, c) for c in children]
        #print(icts)
        g1, g2, g3, g4, g_na = divideToGroups(icts, children, 5/MONTHS, 10/MONTHS, 15/MONTHS)
        #print("BBB", len(g1)+len(g2)+ len(g3)+ len(g4)+ len(g_na))
        m = max(m, (scoreEpsilonByManhattanDistances([g1,g2,g3,g4], heights),e), key=operator.itemgetter(0))
        print("END")
    print(m[1])
    return m[1]


def program(dictionary):
    heights, children = findHeightAroundAge(list(dictionary.swedishChildren))
    print(len(children))
    h1, h2, h3, h4, h_na = divideToGroups(heights, children, -2, 0, 2)
    heights = [h1, h2, h3, h4, h_na]
    print("AAA", len(h1)+ len(h2)+ len(h3)+ len(h4))
    epsilons = [x / 1000 for x in range(50, 105, 5)]
    ictHeightCorrelation(epsilons, children, heights)

    RESTARTS = 10
    # search.local.hill_climbing_random_restarts(,RESTARTS)

