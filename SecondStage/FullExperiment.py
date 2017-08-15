from random import shuffle
from SecondStage.experimentProgram import program as expProg


# Perform the additional stage (post hoc stage):
def postHocStage(numOfFolds, swedishChildrenList, israeliChildrenList, printMode):
    shuffle(swedishChildrenList)
    chunk = int(len(swedishChildrenList) / numOfFolds)
    splitSwedish = [swedishChildrenList[i:i + chunk] for i in range(0, len(swedishChildrenList), chunk)]
    testGroup = [c for c in israeliChildrenList]
    for i in range(0, numOfFolds):
        print("Current group is", i)
        testGroup += splitSwedish[i]
        expGroup = swedishChildrenList[:i] + swedishChildrenList[i+1:]
        sorted(expGroup)
        expProg(expGroup, testGroup, printMode)
        testGroup = [c for c in israeliChildrenList]


# Perform the full experiment of second Stage
def fullProg(swedishChildrenList, israeliChildrenList, printMode):
    # perform experiment with the swedish children as experiment group and the israeli children as test group
    expProg(swedishChildrenList, israeliChildrenList, printMode)
    # perform the additional stage (post hoc stage)
    if printMode:
        print("Post-hoc Stage: ")
    postHocStage(10, swedishChildrenList, israeliChildrenList, printMode)
