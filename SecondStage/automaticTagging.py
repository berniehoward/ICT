import pickle as pkl
from Parser.auxiliary import NA, MONTHS
from SecondStage.secondStageFunc import findICTWithEpsilonByFormula, createFormulaList
from Parser.auxiliary import picklepath, PICKLE_FILE


def tagSecondStage(bestFormula, bestEpsilon):
    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        swedishChildrenList, israeliChildrenList = pkl.load(pklfile)

    automaticTagging(swedishChildrenList, bestFormula, bestEpsilon)
    automaticTagging(israeliChildrenList, bestFormula, bestEpsilon)

    children = (swedishChildrenList, israeliChildrenList)
    with open(picklepath(PICKLE_FILE), "wb") as pklfile:
        pkl.dump(children, pklfile)


# Return the children list with the automatic tagging
def automaticTagging(children, bestFormula, bestEpsilon):
    for c in children:
        ict = findICTWithEpsilonByFormula(bestEpsilon, createFormulaList(bestFormula, c))
        if ict > 20 / MONTHS:
            ict = NA
        c.autoICT = ict
    return children

