from Parser.auxiliary import MONTHS
from FirstStage.firstStageFunc import *
from scipy import stats
from simpleai import search
import operator

def findChildGroup(c, heights): # c - heights of groups
    for g in heights:
        if c in g and heights.index(g):
            return heights.index(g)
    return NA

def scoreEpsilonByManhattanDistances(dbe, heights): #score epsilon values using manhathan distances
    sum = 0
    for g in dbe: #group in dividedByEpsilon
        for c in g:
            #print(c.id, dbe.index(g), findChildGroup(c,heights))
            sum += abs(dbe.index(g) - findChildGroup(c,heights))
    #print(sum)
    return sum

def ictHeightCorrelation(epsilons, children, heights, function=findICTWithEpsilonByBurst):
    m = (NA, NA)
    for e in epsilons:
        #print("EPSILON =", e)
        icts = [function(e, c) for c in children]
        g1, g2, g3, g4, g_na = divideToGroups(icts, children, 5/MONTHS, 10/MONTHS, 15/MONTHS)
        m = max(m, (scoreEpsilonByManhattanDistances([g1,g2,g3,g4], heights),e), key=operator.itemgetter(0))
    return m


def program(dictionary):
    heights, children = findHeightAroundAge(list(dictionary.swedishChildren))
    h1, h2, h3, h4, h_na = divideToGroups(heights, children, -2, 0, 2)
    heights = [h1, h2, h3, h4, h_na]
    epsilons = [x / 1000 for x in range(50, 305, 5)]
    (score1, eps1) = ictHeightCorrelation(epsilons, children, heights)
    (score2, eps2) = ictHeightCorrelation(epsilons, children, heights, findICTWithEpsilonByBurstFor1)
    (score3, eps3) = ictHeightCorrelation(epsilons, children, heights, findICTWithEpsilonByBurstFor2)
    RESTARTS = 10
#    search.local.hill_climbing_random_restarts(,RESTARTS)

