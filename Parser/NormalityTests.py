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

