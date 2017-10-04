import pickle as pkl

from Parser.auxiliary import picklepath, PICKLE_FILE
from Parser.parsingStage import parsingStage
from SecondStage.childrenStatistics import printSampleListStatistics
from SecondStage.fullExperiment import fullProg as secondStage
from SecondStage.automaticTagging import tagSecondStage
# from LearningStage.learningProgram import createRandomForestRegressorAndClassifyData as ThirdStage
from LearningStage.experimentProgram import program as thirdStageProg
from LearningStage.experimentProgram import createFinalRF, tagChildrenValueWithRegressionForest

if __name__ == '__main__':
    # parsingStage() # First stage

    # printSampleListStatistics(swedishChildrenList, israeliChildrenList)
    # secondStage(swedishChildrenList, israeliChildrenList, True) # Second stage

    bestEpsilon = 0.016
    bestFormula = 3
    # tagSecondStage(bestFormula, bestEpsilon) # Tagging stage by Epsilon and Formula

    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        swedishChildrenList, israeliChildrenList = pkl.load(pklfile)

    thirdStageProg(swedishChildrenList, israeliChildrenList) # Learning Stage - Random Forest, Adaboost and SVM

    # createFinalRF(israeliChildrenList, swedishChildrenList)
    # tagChildren(israeliChildrenList, swedishChildrenList)