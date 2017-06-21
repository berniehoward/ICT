from SecondStage.printFunc import *
from SecondStage.searchEpsilon import SearchEpsilon
from SecondStage.secondStageFunc import *
from simpleai.search.local import hill_climbing_random_restarts, hill_climbing


# Experiment program for second stage
def program(setOfChildren):
    childrenList = sorted(list(setOfChildren.swedishChildren))
    heights, indexes = findHeightAroundAge(childrenList)

    # Reorganized children by the order of indexes list
    children = []
    for index in indexes:
        children.append(childrenList[index])

    ####################################################################################################################
    # First method - bins!

    # Divide children to heights groups
    h1, h2, h3, h4, h_na = divideToGroups(heights, children, -1, 0, 1)
    heights_groups = [h1, h2, h3, h4, h_na]  # (At each group there are children)

    # Find first epsilon for each formula
    epsilons = [x / 1000 for x in range(20, 305, 5)]
    eps1, score1 = findEpsilonByFormula(epsilons, children, heights_groups, 1)
    eps2, score2 = findEpsilonByFormula(epsilons, children, heights_groups, 2)
    eps3, score3 = findEpsilonByFormula(epsilons, children, heights_groups, 3)
    printFirstEpsilonPerFormula(eps1, eps2, eps3, score1, score2, score3, True)

    # Find best epsilon for each formula
    problem1 = SearchEpsilon(eps1, score1, 1, children, heights_groups)
    problem2 = SearchEpsilon(eps2, score2, 2, children, heights_groups)
    problem3 = SearchEpsilon(eps3, score3, 3, children, heights_groups)
    bestEps1, bestScore1 = hill_climbing(problem1, 500).state
    bestEps2, bestScore2 = hill_climbing(problem2, 500).state
    bestEps3, bestScore3 = hill_climbing(problem3, 500).state

    # Find best formula
    best_scores = [bestScore1, bestScore2, bestScore3]
    best_epsilons = [bestEps1, bestEps2, bestEps3]
    bestScore = max(best_scores)
    best_formula = best_scores.index(bestScore)
    printBestFormula(best_formula, best_epsilons, bestScore, True)

    # Calculate new ICT:
    newICT = calculateNewICT(childrenList, best_epsilons[best_formula], best_formula + 1)  # List of (child, newICT)
    printCompareToPreviousICT(newICT, True)

    # ####################################################################################################################
    # # Second Method - Regular manhattan dist!
    #
    # print("###########################################################################################################")
    #
    # # Find first epsilon for each formula
    # WITHOUT_BINS = False
    # eps1, score1 = findEpsilonByFormula(epsilons, children, heights, 1, WITHOUT_BINS)
    # eps2, score2 = findEpsilonByFormula(epsilons, children, heights, 2, WITHOUT_BINS)
    # eps3, score3 = findEpsilonByFormula(epsilons, children, heights, 3, WITHOUT_BINS)
    # printFirstEpsilonPerFormula(eps1, eps2, eps3, score1, score2, score3, True)
    #
    # # Find best epsilon for each formula
    # problem1 = SearchEpsilon(eps1, score1, 1, children, heights, WITHOUT_BINS)
    # problem2 = SearchEpsilon(eps2, score2, 2, children, heights, WITHOUT_BINS)
    # problem3 = SearchEpsilon(eps3, score3, 3, children, heights, WITHOUT_BINS)
    # bestEps1, bestScore1 = hill_climbing_random_restarts(problem1, 50, 500).state
    # bestEps2, bestScore2 = hill_climbing_random_restarts(problem2, 50, 500).state
    # bestEps3, bestScore3 = hill_climbing_random_restarts(problem3, 50, 500).state
    #
    # # Find best formula
    # best_scores = [bestScore1, bestScore2, bestScore3]
    # best_epsilons = [bestEps1, bestEps2, bestEps3]
    # bestScore = max(best_scores)
    # best_formula = best_scores.index(bestScore)
    # printBestFormula(best_formula, best_epsilons, bestScore, True)
    #
    # # Calculate new ICT:
    # newICT = calculateNewICT(childrenList, best_epsilons[best_formula], best_formula + 1)  # List of (child, newICT)
    # printCompareToPreviousICT(newICT, True)