from random import shuffle
from SecondStage.experimentProgram import program as expProg
from SecondStage.k_fold import program as k_fold_expProg

# Perform a k-fold additional stage (post hoc stage):
def postHocStage(numOfFolds, swedishChildrenList, israeliChildrenList, printMode):
    shuffle(swedishChildrenList)
    chunk = int(len(swedishChildrenList) / numOfFolds)
    splitSwedish = [swedishChildrenList[i:i + chunk] for i in range(0, len(swedishChildrenList), chunk)]
    for i in range(0, numOfFolds):
        print("Current group is", i)
        expGroup = splitSwedish[:i] + splitSwedish[i+1:]
        expGroup = sum(expGroup, [])
        sorted(expGroup)
        k_fold_expProg(expGroup, splitSwedish[i], printMode)

# Perform the full experiment of second Stage
def fullProg(swedishChildrenList, israeliChildrenList, printMode):
    # perform experiment with the swedish children as experiment group and the israeli children as test group
    # expProg(swedishChildrenList, israeliChildrenList, printMode)
    # perform the additional stage (post hoc stage)
    if printMode:
        print("######################################################################################################")
        print("Post-hoc k-fold Stage: ")
    postHocStage(5, swedishChildrenList, israeliChildrenList, printMode)
