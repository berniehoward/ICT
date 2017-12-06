import pickle as pkl

from Parser.auxiliary import picklepath, PICKLE_FILE
from Parser.parsingStage import parsingStage
from SecondStage.childrenStatistics import printSampleListStatistics
from SecondStage.fullExperiment import fullProg as secondStage
from SecondStage.automaticTagging import tagSecondStage
# from LearningStage.learningProgram import createRandomForestRegressorAndClassifyData as ThirdStage
from LearningStage.experimentProgram import createFinal, tagChildrenValueWithRegressionForest,\
    tagIsraeliWithSwedish
from LearningStage.RFclassifier import RandomForestAlgorithm
from LearningStage.ABclassifier import AdaBoostAlgorithm
from LearningStage.recommendedClassifier import RecommendedAlgorithm
from FourthStage.fourthStageExp import experimentProgram as fourthStage
from LearningStage.utility import *

if __name__ == '__main__':
    # parsingStage()  # First stage

    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        swedishChildrenList, israeliChildrenList = pkl.load(pklfile)

    # secondStage(swedishChildrenList, israeliChildrenList, True)  # Second stage experiment
    bestEpsilon = 0.016
    bestFormula = 3
    # tagSecondStage(bestFormula, bestEpsilon)  # Tagging stage by Epsilon and Formula

    # printSampleListStatistics(swedishChildrenList, israeliChildrenList)
    thirdStageProg(swedishChildrenList, israeliChildrenList)  # Learning Stage - Random Forest and Adaboost
    # tagIsraeliWithSwedish(israeliChildrenList, swedishChildrenList)

    # isr_class_args = 57, 0.1, 20, 5, 14
    # isr_reg_args = 143, 0.8, 20, 10, 17
    # swe_class_args = 84, 0.55, 42, 15, 12
    # swe_reg_args = 45, 0.85, 16, 30, 13
    # params = isr_class_args, isr_reg_args, swe_class_args, swe_reg_args
    # createFinal(israeliChildrenList, swedishChildrenList, params, RandomForestAlgorithm, PICKLE_RANDOM_FOREST_FILE)
    # tagChildrenValueWithRegressionForest(israeliChildrenList, swedishChildrenList, PICKLE_RANDOM_FOREST_FILE)

    # isr_class_args = 22, 113, 35, 0.3, 2, 10
    # isr_reg_args = 24, 141, 12, 0.75, 10, 10
    # swe_class_args = 12, 72, 12, 0.7, 2, 20
    # swe_reg_args = 13, 11, 4, 0.8, 12, 15
    # params = isr_class_args, isr_reg_args, swe_class_args, swe_reg_args
    # createFinal(israeliChildrenList, swedishChildrenList, params, AdaBoostAlgorithm, PICKLE_ADABOOST_FILE)
    # tagChildrenValueWithRegressionForest(israeliChildrenList, swedishChildrenList, PICKLE_ADABOOST_FILE)
    # swe_reg_args = 13, -1, 45, 0.85, 16, 30
    # params = isr_class_args, isr_reg_args, swe_class_args, swe_reg_args
    # createFinal(israeliChildrenList, swedishChildrenList, params, RecommendedAlgorithm, PICKLE_RECOMMENDED_FILE)
    # tagChildrenValueWithRegressionForest(israeliChildrenList, swedishChildrenList, PICKLE_RECOMMENDED_FILE)

    # tagIsraeliWithSwedish(israeliChildrenList, swedishChildrenList)

    # Forth Stage:
    fourthStage(israeliChildrenList, swedishChildrenList)


