import pickle as pkl

from Parser.auxiliary import picklepath, PICKLE_FILE
from Parser.parsingStage import parsingStage
from SecondStage.childrenStatistics import printSampleListStatistics
from SecondStage.fullExperiment import fullProg as secondStage
from SecondStage.automaticTagging import automaticTagging
# from LearningStage.learningProgram import createRandomForestRegressorAndClassifyData as ThirdStage
from LearningStage.experimentProgram import program as thirdStageProg
from LearningStage.experimentProgram import createFinalRF

if __name__ == '__main__':
    # parsingStage()

    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        swedishChildrenList, israeliChildrenList = pkl.load(pklfile)

    # printSampleListStatistics(swedishChildrenList, israeliChildrenList)
    # secondStage(swedishChildrenList, israeliChildrenList, True)

    # bestEpsilon = 0.017083
    bestEpsilon = 0.016
    bestFormula = 3

    automaticTagging(swedishChildrenList, bestFormula, bestEpsilon)
    automaticTagging(israeliChildrenList, bestFormula, bestEpsilon)
    #thirdStageProg(swedishChildrenList, israeliChildrenList)
    createFinalRF(israeliChildrenList, swedishChildrenList)