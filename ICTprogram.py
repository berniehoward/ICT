import pickle as pkl
from Parser.set import childrenSet
from Parser.swedishParsing import parseSwedish
from Parser.israelParsing import parseIsraeli
from Parser.auxiliary import picklepath, PICKLE_FILE, MONTHS
from SecondStage.experimentProgram import program as secondStage
from SecondStage.automaticTagging import automaticTagging
from random import shuffle

# Exacting the parsing stage
def parsingStage():
    setOfChildren = childrenSet()
    setOfChildren.swedishChildren = parseSwedish()
    setOfChildren.israeliChildren = parseIsraeli()
    with open(picklepath(PICKLE_FILE), "wb") as pklfile:
        pkl.dump(setOfChildren, pklfile)


# Return sorted lists of children
def sortListsOfChildren(setOfChildren):
    swedishChildrenList = sorted(list(setOfChildren.swedishChildren))
    israeliChildrenList = sorted(list(setOfChildren.israeliChildren))
    for c in swedishChildrenList:
        c.goodSamples = sorted(c.goodSamples)
    for c in israeliChildrenList:
        c.goodSamples = sorted(c.goodSamples)
    # Remove children without enough samples
    for c in israeliChildrenList:
        if len(c.goodSamples) == 0:
            israeliChildrenList.remove(c)
        else:
            samples = [s for s in c.goodSamples]
            if samples[-1].age < 14 / MONTHS:
                israeliChildrenList.remove(c)
    return swedishChildrenList, israeliChildrenList


def printSamples(list):
    for c in list:
        for s in c.goodSamples:
            print(c, s)
        print()

def k_fold(k, swedishChildrenList, israeliChildrenList):
    shuffle(swedishChildrenList)
    chunk = int(len(swedishChildrenList)/k)
    splitSwedish = [swedishChildrenList[i:i + chunk] for i in range(0, len(swedishChildrenList), chunk)]
    testGroup = [c for c in israeliChildrenList]
    for i in range(0,k):
        print("Current group is", i)
        testGroup += splitSwedish[i]
        expGroup = swedishChildrenList[:i] + swedishChildrenList[i+1:]
        sorted(expGroup)
        secondStage(expGroup, testGroup, True)
        testGroup = [c for c in israeliChildrenList]

if __name__ == '__main__':
    #parsingStage()
    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        setOfChildren = pkl.load(pklfile)
    swedishChildrenList, israeliChildrenList = sortListsOfChildren(setOfChildren)
    #automaticTagging(swedishChildrenList)
    #automaticTagging(israeliChildrenList)
    #secondStage(swedishChildrenList, israeliChildrenList, True)

    ####### K FOLD ######
    # k = 10
    # k_fold(k, swedishChildrenList, israeliChildrenList)

    secondStage(swedishChildrenList, swedishChildrenList+israeliChildrenList, True)