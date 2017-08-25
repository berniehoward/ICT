import pickle as pkl
from Parser.set import childrenSet
from Parser.swedishParsing import parseSwedish
from Parser.israelParsing import parseIsraeli
from Parser.auxiliary import picklepath, PICKLE_FILE, MONTHS


# Return sorted lists of children without children that don't have enough samples
def sortListsOfChildren(setOfChildren):
    swedishChildrenList = sorted(list(setOfChildren.swedishChildren))
    israeliChildrenList = sorted(list(setOfChildren.israeliChildren))
    for c in swedishChildrenList:
        if len(c.heightToAgeBurstFormula1) < 3:
            swedishChildrenList.remove(c)
        c.goodSamples = sorted(c.goodSamples)
    # Remove children without enough samples
    for c in israeliChildrenList:
        c.goodSamples = sorted(c.goodSamples)
        if len([x for x in c.goodSamples if x.age > 0.35]) < 3:
            israeliChildrenList.remove(c)
        else:
            samples = [s for s in [x for x in c.goodSamples if x.age > 0.35]]
            if samples[-1].age < 14 / MONTHS:
                israeliChildrenList.remove(c)
    return swedishChildrenList, israeliChildrenList


# Exacting the parsing stage
def parsingStage():
    setOfChildren = childrenSet()
    setOfChildren.swedishChildren = parseSwedish()
    setOfChildren.israeliChildren = parseIsraeli()
    lists = sortListsOfChildren(setOfChildren)
    with open(picklepath(PICKLE_FILE), "wb") as pklfile:
        pkl.dump(lists, pklfile)

