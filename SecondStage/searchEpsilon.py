from random import randrange
from simpleai.search import SearchProblem
from Parser.auxiliary import MONTHS
from SecondStage.secondStageFunc import findICTWithEpsilonByFormula, createFormulaList, divideToGroups, \
    scoreEpsilonByGroupDistances
import numpy
from operator import itemgetter


# Aid class for hill_climbing_random_restarts created by the 'simpleai' algorithm demands
class SearchEpsilon(SearchProblem):

    def __init__(self, epsilon, score, formulaNum, children, heights_groups, WITHOUT_BINS=True):
        self.first_state = epsilon, score
        self.initial_state = epsilon, score
        self.formula_nam = formulaNum
        self.children = children
        self.heights_groups = heights_groups
        self.WITHOUT_BINS = WITHOUT_BINS

    def initial_state(self):
        return self.first_state

    def actions(self, state):
        epsilon1, score1 = state
        first_epsilon, first_score = self.first_state
        new_epsilons = [x / 1000 for x in range(int((epsilon1 * 1000) - 10), int((epsilon1 * 1000) + 10), 1)]
        new_epsilons = [x for x in new_epsilons if (first_epsilon - 0.005) <= x <= (first_epsilon + 0.005) and x>0]
        new_scores = []
        for e in new_epsilons:
            icts = [findICTWithEpsilonByFormula(e, createFormulaList(self.formula_nam, c)) for c in self.children]
            icts_without_na = [p for p in icts if p > 0]
            median = numpy.median(icts_without_na)
            if not (5 / MONTHS <= median <= 11 / MONTHS):
                new_scores.append(0)
            else:
                if self.WITHOUT_BINS:
                    g1, g2, g3, g4, g_na = divideToGroups(icts, self.children, 6.5 / MONTHS, 9.5 / MONTHS, 11 / MONTHS)
                    new_scores.append(scoreEpsilonByGroupDistances([g1, g2, g3, g4], self.heights_groups))
                else:
                    child_ict = []
                    child_height = []
                    for c, ict in zip(self.children, icts):
                        child_ict.append((c.id, ict))
                    for c, h in zip(self.children, self.heights_groups):
                        child_height.append((c.id, h))
                    new_scores.append(scoreEpsilonByGroupDistances(sorted(child_ict, key=itemgetter(1)), \
                                                               sorted(child_height, key=itemgetter(1)), 2))

        return [(x, y) for x, y in zip(new_epsilons, new_scores)]

    def result(self, state, action):
        return action

    def value(self, state):
        epsilon1, score1 = state
        return score1

    def generate_random_state(self):
        first_epsilon, first_score = self.first_state
        epsilon = randrange(int((first_epsilon * 1000) - 10), int((first_epsilon * 1000) + 10), 1) / 1000
        icts = [findICTWithEpsilonByFormula(epsilon, createFormulaList(self.formula_nam, c)) for c in self.children]
        icts_without_na = [p for p in icts if p > 0]
        median = numpy.median(icts_without_na)
        if not (5 / MONTHS <= median <= 11 / MONTHS):
            score = 0
        else:
            g1, g2, g3, g4, g_na = divideToGroups(icts, self.children, 6.5 / MONTHS, 9.5 / MONTHS, 11 / MONTHS)
            score = scoreEpsilonByGroupDistances([g1, g2, g3, g4], self.heights_groups)
        return epsilon, score


