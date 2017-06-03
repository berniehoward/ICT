from SecondStage.searchEpsilon import SearchEpsilon
from SecondStage.secondStageFunc import *
from simpleai.search.local import hill_climbing_random_restarts


# Main program for second stage
def program(dictionary):
    listOfChildren = list(dictionary.swedishChildren)
    heights, indexes = findHeightAroundAge(listOfChildren)

    # Reorganized children by the order of indexes list
    children = []
    for index in indexes:
        children.append(listOfChildren[index])

    # Divide children to heights groups
    h1, h2, h3, h4, h_na = divideToGroups(heights, children, -1, 0, 1)
    heights_groups = [h1, h2, h3, h4, h_na]  # (At each group there are children)

    # Find first epsilon for each formula
    epsilons = [x / 1000 for x in range(20, 305, 5)]
    eps1, score1 = findEpsilonByFormula(epsilons, children, heights_groups, 1)
    eps2, score2 = findEpsilonByFormula(epsilons, children, heights_groups, 2)
    eps3, score3 = findEpsilonByFormula(epsilons, children, heights_groups, 3)

    # Find best epsilon for each formula
    problem1 = SearchEpsilon(eps1, score1, 1, children, heights_groups)
    problem2 = SearchEpsilon(eps2, score2, 2, children, heights_groups)
    problem3 = SearchEpsilon(eps3, score3, 3, children, heights_groups)
    bestEps1, bestScore1 = hill_climbing_random_restarts(problem1, 50, 500)
    bestEps2, bestScore2 = hill_climbing_random_restarts(problem2, 50, 500)
    bestEps3, bestScore3 = hill_climbing_random_restarts(problem3, 50, 500)

    # Find best formula
    best_scores = [bestScore1, bestScore2, bestScore3]
    best_epsilons = [bestEps1, bestEps2, bestEps3]
    bestScore = max(best_scores)
    best_formula = best_scores.index(bestScore)
    print("Best formula is formula number: ", best_formula + 1)
    print("Best epsilon is: ", best_epsilons[best_formula], " with score: ", bestScore)
