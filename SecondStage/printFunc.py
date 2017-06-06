from partd import numpy
from scipy import stats
from Parser.auxiliary import NA, MONTHS
from Utility import find_nearest


# Checks if the heights lists (in age 6 months and 7 years) are normally distributed
def normalityTests(listOfChildren):
    six_months_heights = []
    seven_years_heights = []
    for child in listOfChildren:
        child.calculateBurst()  # on the fly
        six_idx = find_nearest([a.age for a in child.goodSamples], 0.6)
        if abs(child.goodSamples[six_idx].age - 0.5) < 0.1:
            six_months_heights.append(child.goodSamples[six_idx].height)
        seven_idx = find_nearest([a.age for a in child.goodSamples], 7)
        if abs(child.goodSamples[seven_idx].age - 7) < 0.3:
            seven_years_heights.append(child.goodSamples[seven_idx].height)

    print("result for heights of children at age 6 months: ", stats.mstats.normaltest(six_months_heights))
    print("result for heights of children at age 7 years: ", stats.mstats.normaltest(seven_years_heights))


# Print the first epsilon for each formula
def printFirstEpsilonPerFormula(eps1, eps2, eps3, score1, score2, score3, mode=False):
    if not mode:
        return
    print("first formula: epsilon: ", eps1, ", score: ", score1)
    print("second formula: epsilon: ", eps2, ", score: ", score2)
    print("third formula: epsilon: ", eps3, ", score: ", score3)


# Print the details of the best formula after doing "hill-climbing" algorithm
def printBestFormula(best_formula, best_epsilons, bestScore, mode=False):
    if not mode:
        return
    print("Best formula is formula number: ", best_formula + 1)
    print("Best epsilon is: ", best_epsilons[best_formula], " with score: ", bestScore)


# Print result of comparing for the previous ict tagging
def printCompareToPreviousICT(icts):
    distFromICTz = []
    distFromICTa = []
    distFromICTmin = []
    distFromICTmax = []
    distFromICTavg = []
    count_new_na = 0
    count_previous_z_na = 0
    count_previous_a_na = 0

    for c, ict in icts:
        if ict == NA:
            count_new_na += 1
            continue

        if c.ICT_Z == NA:
            count_previous_z_na += 1
            if c.ICT_A == NA:
                count_previous_a_na += 1
            continue

        distFromICTz.append(abs(c.ICT_Z - ict))

        if c.ICT_A == NA:
            count_previous_a_na += 1
            continue

        distFromICTa.append(abs(c.ICT_A - ict))
        distFromICTmin.append(abs(c.ICT_MIN - ict))
        distFromICTmax.append(abs(c.ICT_MAX - ict))
        distFromICTavg.append(abs(c.ICT_AVG - ict))

    icts_without_na = [p for c, p in icts if p != NA]
    z_icts_without_na = [c.ICT_Z for c, p in icts if c.ICT_Z != NA]
    a_icts_without_na = [c.ICT_A for c, p in icts if c.ICT_A != NA]

    print("New ict median: ", numpy.median(icts_without_na) * MONTHS, ", avg: ", numpy.average(icts_without_na)* MONTHS)
    print("Ze'ev's ict tagging median: ", numpy.median(z_icts_without_na) * MONTHS, ", avg: ",
          numpy.average(z_icts_without_na) * MONTHS)
    print("Alina's ict tagging median: ", numpy.median(a_icts_without_na) * MONTHS, ", avg: ",
          numpy.average(a_icts_without_na) * MONTHS)
    print("Number of NA tags in new tagging process: ", count_new_na)
    print("Number of NA tags in Ze'ev's tagging process: ", count_previous_z_na)
    print("Number of NA tags in Alina's tagging process: ", count_previous_a_na)
    print("Average distance of new tagging process from Ze'ev's tagging process: ", numpy.average(distFromICTz))
    print("Average distance of new tagging process from Alina's tagging process: ", numpy.average(distFromICTa))
    print("Average distance of new tagging process from Ze'ev and Alina average tagging: ", numpy.average(distFromICTavg))
    print("Average distance of new tagging process from Ze'ev and Alina minimum tagging: ", numpy.average(distFromICTmin))
    print("Average distance of new tagging process from Ze'ev and Alina maximum tagging: ", numpy.average(distFromICTmax))


