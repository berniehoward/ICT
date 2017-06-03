from scipy import stats
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
def printFirstEpsilonPerFormula(eps1, eps2, eps3, score1, score2, score3):
    print("first formula: epsilon: ", eps1, ", score: ", score1)
    print("second formula: epsilon: ", eps2, ", score: ", score2)
    print("third formula: epsilon: ", eps3, ", score: ", score3)

