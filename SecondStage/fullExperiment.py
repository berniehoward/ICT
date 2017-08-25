from random import shuffle
from SecondStage.experimentProgram import program as expProg

# Perform a k-fold additional stage (post hoc stage):
def postHocStage(numOfFolds, swedishChildrenList, israeliChildrenList, printMode):
    shuffle(swedishChildrenList)
    chunk = int(len(swedishChildrenList) / numOfFolds)
    splitSwedish = [swedishChildrenList[i:i + chunk] for i in range(0, len(swedishChildrenList), chunk)]
    for i in range(0, numOfFolds):
        print("Current group is", i)
        expGroup = swedishChildrenList[:i] + swedishChildrenList[i+1:]
        sorted(expGroup)
        expProg(expGroup, splitSwedish[i], printMode)


# Perform the full experiment of second Stage
def fullProg(swedishChildrenList, israeliChildrenList, printMode):
    # perform experiment with the swedish children as experiment group and the israeli children as test group
    expProg(swedishChildrenList, israeliChildrenList, printMode)
    # perform the additional stage (post hoc stage)
    #if printMode:
    #    print("######################################################################################################")
     #   print("Post-hoc k-fold Stage: ")
    #postHocStage(10, swedishChildrenList, israeliChildrenList, printMode)
