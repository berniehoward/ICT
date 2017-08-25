from statistics import stdev
from numpy import average, median
from Parser.auxiliary import NA, MONTHS
from Utility import find_nearest
import numpy, scipy


# Print the first epsilon for each formula
def printFirstEpsilonPerFormula(eps1, eps2, eps3, eps4, score1, score2, score3, score4, mode=False):
    if not mode:
        return
    print("First epsilon for each formula: ")
    print("first formula: epsilon: ", eps1, ", score: ", score1)
    print("second formula: epsilon: ", eps2, ", score: ", score2)
    print("third formula: epsilon: ", eps3, ", score: ", score3)
    print("fourth formula: epsilon: ", eps4, ", score: ", score4)
    print()

# Print the details of the best formula after doing "hill-climbing" algorithm
def printBestFormula(best_formula, best_epsilons, bestScore, mode=False):
    if not mode:
        return
    print("Best formula is formula number: ", best_formula + 1)
    print("Best epsilon is: ", best_epsilons[best_formula], " with score: ", bestScore)
    print()


# Print result of comparing for the previous ict tagging
def printCompareToPreviousICT(icts, mode=False):
    if not mode:
        return

    count_new_na = 0
    count_previous_z_na = 0
    count_previous_a_na = 0

    for c, ict in icts:
        if ict == NA:
            count_new_na += 1
        if c.ICT_Z == NA:
            count_previous_z_na += 1
        if c.ICT_A == NA:
            count_previous_a_na += 1

    icts_without_na = [p for c, p in icts if p != NA]
    z_icts_without_na = [c.ICT_Z for c, p in icts if c.ICT_Z != NA]
    a_icts_without_na = [c.ICT_A for c, p in icts if c.ICT_A != NA]
    avg_m = lambda n: average(n)*MONTHS

    print("New ict median: ", median(icts_without_na) * MONTHS, ", avg: ", average(icts_without_na) * MONTHS)
    print("Ze'ev's ict tagging median: ", median(z_icts_without_na) * MONTHS, ", avg: ", avg_m(z_icts_without_na))
    print("Alina's ict tagging median: ", median(a_icts_without_na) * MONTHS, ", avg: ", avg_m(a_icts_without_na))
    print("Number of NA tags in new tagging process: ", count_new_na, " out of ", len(icts))
    print("Number of NA tags in Ze'ev's tagging process: ", count_previous_z_na, " out of ", len(icts))
    print("Number of NA tags in Alina's tagging process: ", count_previous_a_na, " out of ", len(icts))
    print()
    print("The deference between the new tagging to the first expert tagging: ")
    diff_z = [int((p * MONTHS)-(c.ICT_Z * MONTHS)) for c, p in icts if p != NA and c.ICT_Z != NA]
    diff_a = [int((p * MONTHS)-(c.ICT_A * MONTHS)) for c, p in icts if p != NA and c.ICT_A != NA]
    print([diff_z.count(x) for x in range(-12, 12)])
    print([diff_a.count(x) for x in range(-12, 12)])
    print("median: ", median([(p * MONTHS)-(c.ICT_Z * MONTHS) for c, p in icts if p != NA and c.ICT_Z != NA]))
    print("avg: ", average([(p * MONTHS)-(c.ICT_Z * MONTHS) for c, p in icts if p != NA and c.ICT_Z != NA]))
    print("stdev: ", stdev([(p * MONTHS)-(c.ICT_Z * MONTHS) for c, p in icts if p != NA and c.ICT_Z != NA]))

    print([c for c,p in icts if abs((p * MONTHS)-(c.ICT_Z * MONTHS)) > 6 and p != NA and c.ICT_Z != NA])
    print()
    r = [int(p * MONTHS) for p in icts_without_na]
    ict_in_months = [(p * MONTHS) for p in icts_without_na]
    print("kurtosis: ", scipy.stats.kurtosis(ict_in_months))
    print("skew: ", scipy.stats.skew(ict_in_months))
    print("stdev: ",stdev(ict_in_months))
    print([r.count(x) for x in range(1, 21)])
    print()


# Print the score of the experts tagging process
def printExpertsScores(z_score, a_score, printMode):
    if printMode:
        print("The score of Ze'ev's tagging process: ", z_score)
        print("The score of Alina's tagging process: ", a_score)
        print()


# Print the new icts and heights
def printICTAndHeights(newICT, printMode):
    if not printMode:
        return
    print("New ict tags: ")
    print([p * MONTHS for c, p in newICT if p != NA])
    print("heights at age 7 years: ")
    print([c.goodSamples[find_nearest([a.age for a in c.goodSamples], 7)].height for c, p in newICT if p != NA])
    print()

