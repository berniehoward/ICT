from SecondStage.printFunc import *
from SecondStage.searchEpsilon import SearchEpsilon
from SecondStage.secondStageFunc import *
from simpleai.search.local import hill_climbing
import numpy as np

# Perform the discreet method
def discreetMethod(experimentGroup, testChildren, testGroup, heights_groups, t_heights_groups, printMode):
    if printMode:
        print("Discreet Method: ")

    # Find first epsilon for each formula
    epsilons = [x / 1000 for x in range(15, 305, 5)]
    eps1, score1 = findEpsilonByFormula(epsilons, experimentGroup, heights_groups, 1)
    eps2, score2 = findEpsilonByFormula(epsilons, experimentGroup, heights_groups, 2)
    eps3, score3 = findEpsilonByFormula(epsilons, experimentGroup, heights_groups, 3)
    eps4, score4 = findEpsilonByFormula(epsilons, experimentGroup, heights_groups, 4)
    printFirstEpsilonPerFormula(eps1, eps2, eps3, eps4, score1, score2, score3, score4, printMode)

    # Find best epsilon for each formula
    problem1 = SearchEpsilon(eps1, score1, 1, experimentGroup, heights_groups)
    problem2 = SearchEpsilon(eps2, score2, 2, experimentGroup, heights_groups)
    problem3 = SearchEpsilon(eps3, score3, 3, experimentGroup, heights_groups)
    problem4 = SearchEpsilon(eps3, score3, 4, experimentGroup, heights_groups)
    bestEps1, bestScore1 = hill_climbing(problem1, 50).state
    bestEps2, bestScore2 = hill_climbing(problem2, 50).state
    bestEps3, bestScore3 = hill_climbing(problem3, 50).state
    bestEps4, bestScore4 = hill_climbing(problem4, 50).state
    if printMode:
        print("After local search: ")
        print("Formula number 1: Epsilon: ", bestEps1, ", score: ", bestScore1)
        print("Formula number 2: Epsilon: ", bestEps2, ", score: ", bestScore2)
        print("Formula number 3: Epsilon: ", bestEps3, ", score: ", bestScore3)
        print("Formula number 4: Epsilon: ", bestEps4, ", score: ", bestScore4)
        print()

    eps1, k_foldBestScore1 = findEpsilonByFormula([bestEps1], testChildren, t_heights_groups, 1)
    eps2, k_foldBestScore2 = findEpsilonByFormula([bestEps2], testChildren, t_heights_groups, 2)
    eps3, k_foldBestScore3 = findEpsilonByFormula([bestEps3], testChildren, t_heights_groups, 3)
    eps4, k_foldBestScore4 = findEpsilonByFormula([bestEps4], testChildren, t_heights_groups, 4)
    print("Results for best epsilons on test group:\n")
    printFirstEpsilonPerFormula(eps1, eps2, eps3, eps4, k_foldBestScore1, k_foldBestScore2,
                                k_foldBestScore3, k_foldBestScore4, printMode)

    # Find best formula
    best_scores = [k_foldBestScore1, k_foldBestScore2, k_foldBestScore3, k_foldBestScore4]
    best_epsilons = [bestEps1, bestEps2, bestEps3, bestEps4]
    bestScore = max(best_scores)
    best_formula = best_scores.index(bestScore)
    printBestFormula(best_formula, best_epsilons, bestScore, printMode)

    # Calculate new ICT:
    newICT = calculateNewICT(experimentGroup, best_epsilons[best_formula], best_formula + 1)  # List of (child, newICT)
    printCompareToPreviousICT(newICT, printMode)

    # Find the experts scores
    z_score = findScore([c.ICT_Z for c, p in newICT if c.ICT_Z != NA], [c for c, p in newICT if c.ICT_Z != NA],
                        heights_groups, True)
    a_score = findScore([c.ICT_A for c, p in newICT if c.ICT_A != NA], [c for c, p in newICT if c.ICT_A != NA],
                        heights_groups, True)
    printExpertsScores(z_score, a_score, printMode)

    # Print the new icts and heights
    # printICTAndHeights(newICT, printMode)

    # Calculate new ICT for test group children
    testGroupICT = calculateNewICT(testGroup, best_epsilons[best_formula], best_formula + 1)  # List of (child, newICT)
    if printMode:
        print("Test group ICT tagging info: ")
    printCompareToPreviousICT(testGroupICT, printMode)
    return best_formula, best_epsilons[best_formula]


# Perform the sequential method
def sequentialMethod(experimentGroup, testChildren, heights, testGroup, heights_groups, t_heights_groups, printMode):
    if printMode:
        print("Sequential Method: ")
    epsilons = [x / 1000 for x in range(15, 305, 5)]

    # Find first epsilon for each formula
    WITHOUT_BINS = False
    eps1, score1 = findEpsilonByFormula(epsilons, experimentGroup, heights, 1, WITHOUT_BINS)
    eps2, score2 = findEpsilonByFormula(epsilons, experimentGroup, heights, 2, WITHOUT_BINS)
    eps3, score3 = findEpsilonByFormula(epsilons, experimentGroup, heights, 3, WITHOUT_BINS)
    eps4, score4 = findEpsilonByFormula(epsilons, experimentGroup, heights, 4, WITHOUT_BINS)
    printFirstEpsilonPerFormula(eps1, eps2, eps3, eps4, score1, score2, score3, score4, printMode)

    # Find best epsilon for each formula
    problem1 = SearchEpsilon(eps1, score1, 1, experimentGroup, heights, WITHOUT_BINS)
    problem2 = SearchEpsilon(eps2, score2, 2, experimentGroup, heights, WITHOUT_BINS)
    problem3 = SearchEpsilon(eps3, score3, 3, experimentGroup, heights, WITHOUT_BINS)
    problem4 = SearchEpsilon(eps4, score4, 4, experimentGroup, heights, WITHOUT_BINS)
    bestEps1, bestScore1 = hill_climbing(problem1, 50).state
    bestEps2, bestScore2 = hill_climbing(problem2, 50).state
    bestEps3, bestScore3 = hill_climbing(problem3, 50).state
    bestEps4, bestScore4 = hill_climbing(problem4, 50).state
    if printMode:
        print("After local search: ")
        print("Formula number 1: Epsilon: ", bestEps1, ", score: ", bestScore1)
        print("Formula number 2: Epsilon: ", bestEps2, ", score: ", bestScore2)
        print("Formula number 3: Epsilon: ", bestEps3, ", score: ", bestScore3)
        print("Formula number 4: Epsilon: ", bestEps4, ", score: ", bestScore4)
        print()

    eps1, k_foldBestScore1 = findEpsilonByFormula([bestEps1], testChildren, heights, 1, WITHOUT_BINS)
    eps2, k_foldBestScore2 = findEpsilonByFormula([bestEps2], testChildren, heights, 2, WITHOUT_BINS)
    eps3, k_foldBestScore3 = findEpsilonByFormula([bestEps3], testChildren, heights, 3, WITHOUT_BINS)
    eps4, k_foldBestScore4 = findEpsilonByFormula([bestEps4], testChildren, heights, 4, WITHOUT_BINS)
    print("Results for best epsilons on test group:\n")
    printFirstEpsilonPerFormula(eps1, eps2, eps3, eps4, k_foldBestScore1, k_foldBestScore2,
                                k_foldBestScore3, k_foldBestScore4, printMode)
    # Find best formula
    best_scores = [k_foldBestScore1, k_foldBestScore2, k_foldBestScore3, k_foldBestScore4]
    best_epsilons = [bestEps1, bestEps2, bestEps3, bestEps4]
    bestScore = max(best_scores)
    best_formula = best_scores.index(bestScore)
    printBestFormula(best_formula, best_epsilons, bestScore, printMode)

    # Calculate new ICT:
    newICT = calculateNewICT(experimentGroup, best_epsilons[best_formula], best_formula + 1)  # List of (child, newICT)
    printCompareToPreviousICT(newICT, printMode)

    # Find the experts scores
    z_score = findScore([c.ICT_Z for c, p in newICT if c.ICT_Z != NA], [c for c, p in newICT if c.ICT_Z != NA],
                        heights_groups, False)
    a_score = findScore([c.ICT_A for c, p in newICT if c.ICT_A != NA], [c for c, p in newICT if c.ICT_A != NA],
                        heights_groups, False)
    printExpertsScores(z_score, a_score, printMode)

    # Calculate new ICT for children in the test Group
    testGroupICT = calculateNewICT(testGroup, best_epsilons[best_formula], best_formula + 1)  # List of (child, newICT)
    if printMode:
        print("Test Group ICT tagging info: ")
    printCompareToPreviousICT(testGroupICT, printMode)
    return best_formula, best_epsilons[best_formula]

# Experiment program for second stage
def program(experimentGroup, testGroup, printMode=False):

    heights, indexes = findHeightAroundAge(experimentGroup)
    t_heights, t_indexes = findHeightAroundAge(testGroup)
    # Reorganized children by the order of indexes list
    children = []
    t_children = []

    for index in indexes:
        children.append(experimentGroup[index])

    for index in t_indexes:
        t_children.append(testGroup[index])

    # Divide children to heights groups
    h1, h2, h3, h4, h_na = divideToGroups(heights, children, -1, 0, 1)
    heights_groups = [h1, h2, h3, h4, h_na]  # (At each group there are children)

    t_h1, t_h2, t_h3, t_h4, t_h_na = divideToGroups(t_heights, t_children, -1, 0, 1)
    t_heights_groups = [t_h1, t_h2, t_h3, t_h4, t_h_na]  # (At each group there are children)

    best_d_formula, best_d_epsilon = discreetMethod(children, t_children, testGroup, heights_groups, t_heights_groups, printMode)

    if printMode:
        print("#######################################################################################################")
        print()

    best_s_formula, best_s_epsilon = sequentialMethod(children, t_children, heights, testGroup, heights_groups, t_heights_groups, printMode)
    return best_d_formula+1, best_d_epsilon, best_s_formula+1, best_s_epsilon



