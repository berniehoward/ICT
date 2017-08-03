
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


if __name__ == '__main__':
    #parsingStage()

    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        setOfChildren = pkl.load(pklfile)

    swedishChildrenList = sorted(list(setOfChildren.swedishChildren))
    secondStage(setOfChildren.swedishChildren, True)
    #secondStage(setOfChildren.israeliChildren)
