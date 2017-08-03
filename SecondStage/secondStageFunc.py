from Utility import find_nearest
from Parser.auxiliary import NA, MONTHS
from scipy import stats
from operator import itemgetter
import numpy


# Find heights of the children at age 6 months, 6 years, 7 years
def findHeightAroundAge(listOfChildren):
    six_months_heights = []
    six_years_heights = []
    seven_years_heights = []
    for child in listOfChildren:
        if not child.goodSamples:
            continue
        six_months_idx = find_nearest([a.age for a in child.goodSamples], 0.5)
        six_years_idx = find_nearest([a.age for a in child.goodSamples], 6)
        seven_years_idx = find_nearest([a.age for a in child.goodSamples], 7)
        if (abs(child.goodSamples[six_months_idx].age - 0.5) < 0.3) and \
                (abs(child.goodSamples[six_years_idx].age - 6) < 0.8) and \
                (abs(child.goodSamples[seven_years_idx].age - 7) < 0.8):
            six_months_heights.append(child.goodSamples[six_months_idx].height)
            six_years_heights.append(child.goodSamples[six_years_idx].height)
            seven_years_heights.append(child.goodSamples[seven_years_idx].height)
    return normalizeZScore(six_months_heights, six_years_heights, seven_years_heights)


# Normalizes the height lists and subtract it
# Return normalized list of delta heights and list of indexes show the new order of the children's list
def normalizeZScore(six_months_heights, six_years_heights, seven_years_heights):
    # Normalized list of heights at age 6 month
    normalized_six_months_heights = stats.zscore(six_months_heights)

    # Dived into groups by height at age 6 years
    six_years_idx_group1 = []
    six_years_idx_group2 = []
    six_years_idx_group3 = []
    idx = 0
    for h in six_years_heights:
        if h < 1.15:
            six_years_idx_group1.append(idx)
        elif 1.15 <= h <= 1.19:
            six_years_idx_group2.append(idx)
        else:
            six_years_idx_group3.append(idx)
        idx += 1

    # Normalizes height at age 7 years by their group at 6 years
    seven_years_group1 = [seven_years_heights[idx] for idx in six_years_idx_group1]
    seven_years_group2 = [seven_years_heights[idx] for idx in six_years_idx_group2]
    seven_years_group3 = [seven_years_heights[idx] for idx in six_years_idx_group3]
    seven_years_group1 = stats.zscore(seven_years_group1)
    seven_years_group2 = stats.zscore(seven_years_group2)
    seven_years_group3 = stats.zscore(seven_years_group3)
    normalized_seven_months_heights = list(seven_years_group1) + \
                                      list(seven_years_group2) + list(seven_years_group3)

    # Reorganized six months group to be at the order of seven years group
    reorganized_six_months_heights = []
    for idx in six_years_idx_group1:
        reorganized_six_months_heights.append(normalized_six_months_heights[idx])
    for idx in six_years_idx_group2:
        reorganized_six_months_heights.append(normalized_six_months_heights[idx])
    for idx in six_years_idx_group3:
        reorganized_six_months_heights.append(normalized_six_months_heights[idx])

    indexes = six_years_idx_group1 + six_years_idx_group2 + six_years_idx_group3
    return [(h7 - h6) for h7, h6 in zip(normalized_seven_months_heights, \
            reorganized_six_months_heights)], indexes


# Divide to 5 groups according to the borders: b1, b2, b3
def divideToGroups(featureList, children, b1, b2, b3):
    g1 = []
    g2 = []
    g3 = []
    g4 = []
    g_na = []  # don't belong to any group
    for f, c in zip(featureList, children):
        if f == NA:
            g_na.append(c)
        elif f < b1:
            g1.append(c)
        elif b1 <= f <= b2:
            g2.append(c)
        elif b2 <= f <= b3:
            g3.append(c)
        else:
            g4.append(c)
    return g1, g2, g3, g4, g_na


# Find the first age where formula in bigger then epsilon - this age is the ICT point
def findICTWithEpsilonByFormula(e, formulaList):
    for midAge, slope in formulaList:
         if slope > e:
            return midAge
    return NA



# Find the height group of a specific child
def findChildGroup(c, heights_groups):
    for g in heights_groups:
        if c in g and heights_groups.index(g):
            return heights_groups.index(g)
    return NA


# Find the epsilon which cause the largest score
def findEpsilonByFormula(epsilons, children, heights_groups, formulaNum, bins=True):
    scores = []
    for e in epsilons:
        icts = [findICTWithEpsilonByFormula(e, createFormulaList(formulaNum, c)) for c in children]
        icts_without_na = [p for p in icts if p > 0]
        median = numpy.median(icts_without_na)
        if not (5/MONTHS <= median <= 11/MONTHS):
            scores.append(0)
        elif bins:
            g1, g2, g3, g4, g_na = divideToGroups(icts, children, 6.5 / MONTHS, 9.5 / MONTHS, 11 / MONTHS)
            scores.append(scoreEpsilonByGroupDistances([g1, g2, g3, g4], heights_groups, 1))
        else:
            child_ict = []
            child_height = []
            for c, ict in zip(children, icts):
                child_ict.append((c.id, ict))
            for c, h in zip(children, heights_groups):
                child_height.append((c.id, h))
            for i in child_ict: #for removal of NA's
                if(i[1] == NA):
                    c = [c[0] for c in child_height]
                    idx = c.index(i[0])
                    child_height = child_height[:idx] + child_height[idx+1:]
                    child_ict.remove(i)
            scores.append(scoreEpsilonByGroupDistances(sorted(child_ict, key=itemgetter(1)),
                                                       sorted(child_height, key=itemgetter(1)), 2))
    bestScore = max(scores)
    return epsilons[scores.index(bestScore)], bestScore


# Return list of (midAge, slope) of the child by the formula number
def createFormulaList(formulaNum, child):
    if formulaNum == 1:
        return child.heightToAgeBurstFormula1
    elif formulaNum == 2:
        return child.heightToAgeBurstFormula2
    elif formulaNum == 3:
        return child.heightToAgeBurstFormula3
    else:
        return child.heightToAgeBurstFormula4


# Score epsilon values using group distances
def scoreEpsilonByGroupDistances(ict_groups, heights_groups, method=1):
    sum = 0
    if method == 1:
        for g in ict_groups:
            for c in g:
                try:
                    idx1 = ict_groups.index(g)
                except ValueError:
                    continue
                idx2 = findChildGroup(c, heights_groups)
                if idx2 == NA:
                    continue
                sum += abs(idx1 - idx2)
        return sum
    else:
        for c, ict in ict_groups:
            h_current_index = 0
            item = [i for i in heights_groups if i[0] == c]
            for i in item:
                h_current_index = (heights_groups.index(i))
                continue
            sum += abs(ict_groups.index((c, ict)) - h_current_index)
        return sum


# Return a list of tuples (child, newICT)
def calculateNewICT(children, bestEpsilon, bestFormula):
    icts = []
    for c in children:
        ict = findICTWithEpsilonByFormula(bestEpsilon, createFormulaList(bestFormula, c))
        if ict > 20:
            ict = NA
        icts.append((c, ict))
    return icts


# Return the score of a given tagging
def findScore(ict, children, heights_groups, discreetMethod):
    median = numpy.median(ict)
    if not (5 / MONTHS <= median <= 11 / MONTHS):
        return 0
    elif discreetMethod:
        g1, g2, g3, g4, g_na = divideToGroups(ict, children, 6.5 / MONTHS, 9.5 / MONTHS, 11 / MONTHS)
        return scoreEpsilonByGroupDistances([g1, g2, g3, g4], heights_groups, 1)
    else:
        child_ict = []
        child_height = []
        for c, ict in zip(children, ict):
            child_ict.append((c.id, ict))
        for c, h in zip(children, heights_groups):
            child_height.append((c.id, h))
        return scoreEpsilonByGroupDistances(sorted(child_ict, key=itemgetter(1)),
                                            sorted(child_height, key=itemgetter(1)), 2)