from random import shuffle
from SecondStage.experimentProgram import program as expProg
from SecondStage.k_fold import program as k_fold_expProg
from numpy import mean

def most_common(lst):
    return max(set(lst), key=lst.count)

# Perform a k-fold additional stage (post hoc stage):
def postHocStage(numOfFolds, swedishChildrenList, israeliChildrenList, printMode):
    d_results = []
    s_results = []
    for i in range(0,5):
        shuffle(swedishChildrenList)
        chunk = int(len(swedishChildrenList) / numOfFolds)
        splitSwedish = [swedishChildrenList[i:i + chunk] for i in range(0, len(swedishChildrenList), chunk)]
        for i in range(0, numOfFolds):
            print("Current group is", i)
            expGroup = splitSwedish[:i] + splitSwedish[i+1:]
            expGroup = sum(expGroup, [])
            sorted(expGroup)
            best_d_formula, best_d_epsilon, best_s_formula, best_s_epsilon = \
                k_fold_expProg(expGroup, splitSwedish[i], printMode)
            d_results.append((best_d_formula, best_d_epsilon))
            s_results.append((best_s_formula, best_s_epsilon))
    mcd = most_common([x[0] for x in d_results])
    print("Discrete: Max formula is", mcd, "with avg epsilon of ", \
                mean([y[1] for y in [x for x in d_results if x[0]==mcd]]))
    mcs = most_common([x[0] for x in s_results])
    print("Sequential: Max formula is", mcs, "with avg epsilon of ", \
                mean([y[1] for y in [x for x in s_results if x[0]==mcs]]))

# Perform the full experiment of second Stage
def fullProg(swedishChildrenList, israeliChildrenList, printMode):
    # perform experiment with the swedish children as experiment group and the israeli children as test group
    # expProg(swedishChildrenList, israeliChildrenList, printMode)
    # perform the additional stage (post hoc stage)
    if printMode:
        print("######################################################################################################")
        print("Post-hoc k-fold Stage: ")
    postHocStage(5, swedishChildrenList, israeliChildrenList, printMode)
