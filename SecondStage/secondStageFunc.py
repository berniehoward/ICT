from Utility import find_nearest
from Parser.auxiliary import NA, MONTHS
from scipy import stats
import numpy


# Find heights of the children at age 6 months, 6 years, 7 years
def findHeightAroundAge(listOfChildren):
    six_months_heights = []
    six_years_heights = []
    seven_years_heights = []
    for child in listOfChildren:
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
    normalized_seven_months_heights = list(seven_years_group1) + list(seven_years_group2) + list(seven_years_group3)

    # Reorganized six months group to be at the order of seven years group
    reorganized_six_months_heights = []
    for idx in six_years_idx_group1:
        reorganized_six_months_heights.append(normalized_six_months_heights[idx])
    for idx in six_years_idx_group2:
        reorganized_six_months_heights.append(normalized_six_months_heights[idx])
    for idx in six_years_idx_group3:
        reorganized_six_months_heights.append(normalized_six_months_heights[idx])

    indexes = six_years_idx_group1 + six_years_idx_group2 + six_years_idx_group3
    return [(h7 - h6) for h7, h6 in zip(normalized_seven_months_heights, reorganized_six_months_heights)], indexes


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
def findEpsilonByFormula(epsilons, children, heights_groups, formulaNum):
    scores = []
    for e in epsilons:
        icts = [findICTWithEpsilonByFormula(e, createFormulaList(formulaNum, c)) for c in children]
        icts_without_na = [p for p in icts if p > 0]
        median = numpy.median(icts_without_na)
        if not (5/MONTHS <= median <= 11/MONTHS):
            scores.append(0)
        else:
            g1, g2, g3, g4, g_na = divideToGroups(icts, children, 6.5 / MONTHS, 9.5 / MONTHS, 11 / MONTHS)
            scores.append(scoreEpsilonByGroupDistances([g1, g2, g3, g4], heights_groups))
    bestScore = max(scores)
    return epsilons[scores.index(bestScore)], bestScore


# Return list of (midAge, slope) of the child by the formula number
def createFormulaList(formulaNum, child):
    if formulaNum == 1:
        return child.heightToAgeBurstFormula1
    elif formulaNum == 2:
        return child.heightToAgeBurstFormula2
    return child.heightToAgeBurstFormula3


# Score epsilon values using group distances
def scoreEpsilonByGroupDistances(ict_groups, heights_groups):
    sum = 0
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