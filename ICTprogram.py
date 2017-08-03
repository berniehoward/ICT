
import pickle as pkl
from Parser.set import childrenSet
from Parser.swedishParsing import parseSwedish
from Parser.israelParsing import parseIsraeli
from Parser.auxiliary import picklepath, PICKLE_FILE
from SecondStage.experimentProgram import program as secondStage


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
    return swedishChildrenList, israeliChildrenList

if __name__ == '__main__':
    #parsingStage()
    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        setOfChildren = pkl.load(pklfile)
    swedishChildrenList, israeliChildrenList = sortListsOfChildren(setOfChildren)
    secondStage(swedishChildrenList, israeliChildrenList, True)


