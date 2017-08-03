from numpy import average, median
from Parser.auxiliary import NA, MONTHS
from Utility import find_nearest


# Checks if the heights lists (in age 6 months and 7 years) are normally distributed
def swedishNormalityTests(listOfChildren):
    six_months_heights = []
    seven_years_heights = []
    for child in listOfChildren:
        six_idx = find_nearest([a.age for a in child.goodSamples], 0.5)
        if abs(child.goodSamples[six_idx].age - 0.5) < 0.3:
            six_months_heights.append(child.goodSamples[six_idx].height)
        seven_idx = find_nearest([a.age for a in child.goodSamples], 7)
        if abs(child.goodSamples[seven_idx].age - 7) < 0.8:
            seven_years_heights.append(child.goodSamples[seven_idx].height)

    print("Height at age 6 months")
    for x in sorted(list(set(six_months_heights))):
        print(x, ",", len([y for y in six_months_heights if abs(x - y) < 0.05]))

    print("Height at age 7 years")
    for x in sorted(list(set(seven_years_heights))):
        print(x, ",", len([y for y in seven_years_heights if abs(x - y) < 0.05]))
    print()


# Checks if the heights list (in age 6 months) is normally distributed
def israeliNormalityTests(listOfChildren):
    six_months_heights = []
    for child in listOfChildren:
        if len(child.goodSamples) == 0:
            continue
        six_idx = find_nearest([a.age for a in child.goodSamples], 0.5)
        if abs(child.goodSamples[six_idx].age - 0.5) < 0.3:
            six_months_heights.append(child.goodSamples[six_idx].height)

    print("Height at age 6 months: ")
    for x in sorted(list(set(six_months_heights))):
        print(x, ",", len([y for y in six_months_heights if abs(x - y) < 0.05]))
    print()


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
    print("Ze'ev's ict tagging median: ", median(z_icts_without_na) * MONTHS, ", avg: ",
          avg_m(z_icts_without_na))
    print("Alina's ict tagging median: ", median(a_icts_without_na) * MONTHS, ", avg: ",
          avg_m(a_icts_without_na))
    print("Number of NA tags in new tagging process: ", count_new_na)
    print("Number of NA tags in Ze'ev's tagging process: ", count_previous_z_na)
    print("Number of NA tags in Alina's tagging process: ", count_previous_a_na)
    print()


# Print the score of the experts tagging process
def printExpertsScores(z_score, a_score, printMode):
    if printMode:
        print("The score of Ze'ev's tagging process: ", z_score)
        print("The score of Alina's tagging process: ", a_score)
        print()

