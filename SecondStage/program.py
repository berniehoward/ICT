from SecondStage.secondStageFunc import *
from scipy import stats
#from simpleai import search
from random import uniform


# def hill_climbing(initial, children, heights, count = 1000):
#     bestScore, bestEps = initial
#     print("INITBEST:", bestScore, bestEps)
#     for c in range(1,count):
#         r = uniform(-0.003, 0.003)
#         s, e = ictHeightCorrelation([bestEps+r], children, heights)
#         #print("AA", s, e)
#         if s >= bestScore:
#             bestScore, bestEps = s, e
#     print(bestScore,bestEps)
#     return bestScore,bestEps


# Main program for second stage
def program(dictionary):
    listOfChildren = list(dictionary.swedishChildren)
    heights, indexes = findHeightAroundAge(listOfChildren)
    children = []
    for index in indexes:
        children.append(listOfChildren[index])
    h1, h2, h3, h4, h_na = divideToGroups(heights, children, -2, 0, 2)
    print("heights: ", len(h1), len(h2), len(h3), len(h4), len(h_na))
    heights_groups = [h1, h2, h3, h4, h_na]  # At each group there are children
    epsilons = [x / 1000 for x in range(50, 305, 5)]
    eps1, score1 = findEpsilonByFormula(epsilons, children, heights_groups, 1)
    eps2, score2 = findEpsilonByFormula(epsilons, children, heights_groups, 2)
    eps3, score3 = findEpsilonByFormula(epsilons, children, heights_groups, 3)
    print(eps1, score1)
    print(eps2, score2)
    print(eps3, score3)

