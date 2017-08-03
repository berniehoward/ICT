from SecondStage.printFunc import *
from SecondStage.searchEpsilon import SearchEpsilon
from SecondStage.secondStageFunc import *
from simpleai.search.local import hill_climbing


# Experiment program for second stage
def program(children, printMode=False):

    childrenList = sorted(list(children))
    for c in children:
        c.goodSamples = sorted(c.goodSamples)

    heights, indexes = findHeightAroundAge(childrenList)

    # Reorganized children by the order of indexes list
    children = []
    for index in indexes:
        children.append(childrenList[index])

    ############################################# First method - Discreet #############################################

    # Divide children to heights groups
    h1, h2, h3, h4, h_na = divideToGroups(heights, children, -1, 0, 1)
    heights_groups = [h1, h2, h3, h4, h_na]  # (At each group there are children)

    # Find first epsilon for each formula
    epsilons = [x / 1000 for x in range(15, 305, 5)]
    eps1, score1 = findEpsilonByFormula(epsilons, children, heights_groups, 1)
    eps2, score2 = findEpsilonByFormula(epsilons, children, heights_groups, 2)
    eps3, score3 = findEpsilonByFormula(epsilons, children, heights_groups, 3)
    eps4, score4 = findEpsilonByFormula(epsilons, children, heights_groups, 4)
    printFirstEpsilonPerFormula(eps1, eps2, eps3, eps4, score1, score2, score3, score4, printMode)

    # Find best epsilon for each formula
    problem1 = SearchEpsilon(eps1, score1, 1, children, heights_groups)
    problem2 = SearchEpsilon(eps2, score2, 2, children, heights_groups)
    problem3 = SearchEpsilon(eps3, score3, 3, children, heights_groups)
    problem4 = SearchEpsilon(eps3, score3, 4, children, heights_groups)
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

    # Find best formula
    best_scores = [bestScore1, bestScore2, bestScore3, bestScore4]
    best_epsilons = [bestEps1, bestEps2, bestEps3, bestEps4]
    bestScore = max(best_scores)
    best_formula = best_scores.index(bestScore)
    printBestFormula(best_formula, best_epsilons, bestScore, printMode)

    # Calculate new ICT:
    newICT = calculateNewICT(children, best_epsilons[best_formula], best_formula + 1)  # List of (child, newICT)
    printCompareToPreviousICT(newICT, printMode)

    # Find the experts scores
    z_score = findScore([c.ICT_Z for c, p in newICT if c.ICT_Z != NA], [c for c, p in newICT if c.ICT_Z != NA],
                        heights_groups, True)
    a_score = findScore([c.ICT_A for c, p in newICT if c.ICT_A != NA], [c for c, p in newICT if c.ICT_A != NA],
                        heights_groups, True)
    printExpertsScores(z_score, a_score, printMode)

    # print the new icts and delta heights
    if printMode:
        print("New ict tags: ")
        print([p * MONTHS if p != NA else p for c, p in newICT])
        print("Delta heights during childhood: ")
        print(heights)
        print()

    ############################################ Second Method - Sequential  ###########################################

    if printMode:
        print("#######################################################################################################")
        print()

    # Find first epsilon for each formula
    WITHOUT_BINS = False
    eps1, score1 = findEpsilonByFormula(epsilons, children, heights, 1, WITHOUT_BINS)
    eps2, score2 = findEpsilonByFormula(epsilons, children, heights, 2, WITHOUT_BINS)
    eps3, score3 = findEpsilonByFormula(epsilons, children, heights, 3, WITHOUT_BINS)
    eps4, score4 = findEpsilonByFormula(epsilons, children, heights, 4, WITHOUT_BINS)
    printFirstEpsilonPerFormula(eps1, eps2, eps3, eps4, score1, score2, score3, score4, printMode)

    # Find best epsilon for each formula
    problem1 = SearchEpsilon(eps1, score1, 1, children, heights, WITHOUT_BINS)
    problem2 = SearchEpsilon(eps2, score2, 2, children, heights, WITHOUT_BINS)
    problem3 = SearchEpsilon(eps3, score3, 3, children, heights, WITHOUT_BINS)
    problem4 = SearchEpsilon(eps4, score4, 4, children, heights, WITHOUT_BINS)
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

    # Find best formula
    best_scores = [bestScore1, bestScore2, bestScore3, bestScore4]
    best_epsilons = [bestEps1, bestEps2, bestEps3, bestEps4]
    bestScore = max(best_scores)
    best_formula = best_scores.index(bestScore)
    printBestFormula(best_formula, best_epsilons, bestScore, printMode)

    # Calculate new ICT:
    newICT = calculateNewICT(children, best_epsilons[best_formula], best_formula + 1)  # List of (child, newICT)
    printCompareToPreviousICT(newICT, printMode)

    # Find the experts scores
    z_score = findScore([c.ICT_Z for c, p in newICT if c.ICT_Z != NA], [c for c, p in newICT if c.ICT_Z != NA],
                        heights_groups, False)
    a_score = findScore([c.ICT_A for c, p in newICT if c.ICT_A != NA], [c for c, p in newICT if c.ICT_A != NA],
                        heights_groups, False)
    printExpertsScores(z_score, a_score, printMode)

    # print the new icts and delta heights
    if printMode:
        print("New ict tags: ")
        print([p * MONTHS if p != NA else p for c, p in newICT])
        print("Delta heights during childhood: ")
        print(heights)
        print()


