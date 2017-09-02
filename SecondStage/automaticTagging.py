from Parser.auxiliary import NA, MONTHS
from SecondStage.secondStageFunc import findICTWithEpsilonByFormula, createFormulaList


# Return the children list with the automatic tagging
def automaticTagging(children, bestFormula, bestEpsilon):
    for c in children:
        ict = findICTWithEpsilonByFormula(bestEpsilon, createFormulaList(bestFormula, c))
        if ict > 20 / MONTHS:
            ict = NA
        c.autoICT = ict
    return children

