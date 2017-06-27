
import pickle as pkl
from Parser.set import childrenSet
from Parser.parser import print_statistics
from Parser.swedishParsing import parseSwedish
from Parser.israelParsing import parseIsraeli
from Parser.auxiliary import picklepath, PICKLE_FILE
from SecondStage.experimentProgram import program as secondStage

# #For exact the parsing stage uncomment this part :
# if __name__ == '__main__':
#     setOfChildren = childrenSet()
#     setOfChildren.swedishChildren = parseSwedish()
#     #print_statistics("S")
#     #print()
#     setOfChildren.israeliChildren = parseIsraeli()
#     #print_statistics("I")
#     for c in setOfChildren.swedishChildren:
#         print(c.id, [(i.age, i.height) for i in c.goodSamples])
#     with open(picklepath(PICKLE_FILE), "wb") as pklfile:
#         pkl.dump(setOfChildren, pklfile)


if __name__ == '__main__':
    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        setOfChildren = pkl.load(pklfile)

    swedishChildrenList = sorted(list(setOfChildren.swedishChildren))
    #secondStage(setOfChildren.swedishChildren)
    #secondStage(setOfChildren.israeliChildren)
