from LearningStage.classificationExperiment import createBoolClassification, getDataForBooleanClassification
from LearningStage.regressionExperiment import createRegressionClassification, getDataForClassification
from LearningStage.utility import *
from Parser.auxiliary import *
import os
from LearningStage.constants import *
from Parser.auxiliary import MONTHS, NA
import pickle as pkl
from LearningStage.RFclassifier import RandomForestAlgorithm
from statistics import stdev
from numpy import average, median
from LearningStage.classificationRandomForest import booleanTreesExp, booleanTreesTuning, \
    booleanTreesFeatureSelectionAndFinalClassifier
from LearningStage.classificationAdaBoost import booleanAdaExp, booleanAdaTuning, booleanAdaFeatureSelectionAndFinalClassifier
from LearningStage.regressionAdaBoost import regressionAdaExp, regressionAdaTuning, regressionAdaFinalClassifier
from LearningStage.regressionRandomForest import regressionForestExp, regressionForestTuning, regressionRFFinalClassifier
import numpy as np

# TODO - Does all the functions really belong to this file? or we need to move some? maybe file for RF general
# function and file to AdaBoost?


def randomForestExperiment(swedishChildrenList, israeliChildrenList, printMode=False):
    print("Boolean trees: ")
    isr_f, isr_classification_RF, swe_f, swe_classification_RF = \
    createBoolClassification(swedishChildrenList, israeliChildrenList, booleanTreesExp, booleanTreesTuning,
                             booleanTreesFeatureSelectionAndFinalClassifier, BRF_PARM)
    # print("Regression trees: ")
    # isr_f, isr_regression_RF, swe_f, swe_regression_RF = \
    #     createRegressionClassification(swedishChildrenList, israeliChildrenList, regressionForestExp,
    #                                    regressionForestTuning, regressionRFFinalClassifier, RRF_PARM, R_forests, RF_k)
    # if printMode:
    #     exportTreesFromForest(isr_f, isr_regression_RF, Nationality.ISR.name, DecisionAlgorithmType.REGRESSION.name)
    #     exportTreesFromForest(swe_f, swe_regression_RF, Nationality.SWE.name, DecisionAlgorithmType.REGRESSION.name)
    #     exportTreesFromForest(isr_f, isr_classification_RF, Nationality.ISR.name, DecisionAlgorithmType.CLASSIFICATION.value)
    #     exportTreesFromForest(swe_f, swe_classification_RF, Nationality.SWE.name, DecisionAlgorithmType.CLASSIFICATION.value)


def adaBoostExperiment(swedishChildrenList, israeliChildrenList, printMode=False):
    print("Boolean AdaBoost: ")
    isr_f, isr_classification_AB, swe_f, swe_classification_AB = \
        createBoolClassification(swedishChildrenList, israeliChildrenList, booleanAdaExp, booleanAdaTuning,
                                 booleanAdaFeatureSelectionAndFinalClassifier, BAB_PARM)
    # print("Regression AdaBoost: ")
    # isr_f, isr_regression_RF, swe_f, swe_regression_RF = \
    #     createRegressionClassification(swedishChildrenList, israeliChildrenList, regressionAdaExp, regressionAdaTuning,
    #                                    regressionAdaFinalClassifier, RAB_PARM, R_ada, AB_k)


# Perform experiment for the third stage
def program(swedishChildrenList, israeliChildrenList, printMode=False):
    printMode = True
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    # createFeatureHistogram(swedishChildrenList, israeliChildrenList)
    # randomForestExperiment(swedishChildrenList, israeliChildrenList, printMode)
    adaBoostExperiment(swedishChildrenList, israeliChildrenList, printMode)


# Create random forest learning algorithm by parameters found in the experiment
def createFinalRF(israeliChildrenList, swedishChildrenList):
    isr_classi_f, X_classi_isr, c_classi_isr = getDataForBooleanClassification(israeliChildrenList)
    swe_classi_f, X_classi_swe, c_classi_swe = getDataForBooleanClassification(swedishChildrenList)
    isr_regress_f, X_regress_isr, c_regress_isr = getDataForClassification(israeliChildrenList)
    swe_regress_f, X_regress_swe, c_regress_swe = getDataForClassification(swedishChildrenList)
    X_classi_isr, isr_classi_f = removeNationFeature(X_classi_isr, isr_classi_f)
    X_classi_swe, swe_classi_f = removeNationFeature(X_classi_swe, swe_classi_f)
    data = X_classi_isr, c_classi_isr, isr_classi_f, X_regress_isr, c_regress_isr, isr_regress_f, X_classi_swe, \
        c_classi_swe, swe_classi_f, X_regress_swe, c_regress_swe, swe_regress_f
    isr_class_args = 57, 0.1, 20, 5, 14
    isr_reg_args = 143, 0.8, 20, 10, 17
    swe_class_args = 84, 0.55, 42, 15, 12
    swe_reg_args = 45, 0.85, 16, 30, 13
    rf_classifier = RandomForestAlgorithm(data, isr_class_args, isr_reg_args, swe_class_args, swe_reg_args)

    with open(randomforestpath(PICKLE_RANDOM_FOREST_FILE), "wb") as pklfile:
        pkl.dump(rf_classifier, pklfile)


# Tag children with found RF
def tagChildrenValueWithRegressionForest(israeliChildrenList, swedishChildrenList):
    with open(randomforestpath(PICKLE_RANDOM_FOREST_FILE), "rb") as pklfile:
        rf_classifier = pkl.load(pklfile)

    predicted_ICT = []
    for c in israeliChildrenList + swedishChildrenList:
        ict_val = rf_classifier.classifyChild(c)
        c.regICT = ict_val
        predicted_ICT.append(ict_val)
    orig_ICT = [c.autoICT * MONTHS if c.autoICT != NA else c.autoICT for c in (israeliChildrenList + swedishChildrenList)]
    print("Original tagging: ")
    print(orig_ICT)
    print("Predicted tagging: ")
    print(predicted_ICT)
    print("Differences in days: ")
    diff = [int((x-y)*30) for x, y in zip(orig_ICT, predicted_ICT) if x != NA and y != NA]
    print([diff.count(x) for x in range(-70, 70)])
    print("median: ", median(diff))
    print("avg: ", average(diff))
    print("stdev: ", stdev(diff))

    manual_ICT = [c.ICT_Z * MONTHS if c.ICT_Z != NA else c.ICT_Z for c in (israeliChildrenList + swedishChildrenList)]
    print("Manual tagging: ")
    print(manual_ICT)
    print("Differences in days: ")
    diff = [int((x - y) * 30) for x, y in zip(manual_ICT, predicted_ICT) if x != NA and y != NA]
    print([diff.count(x) for x in range(-70, 70)])
    print("median: ", median(diff))
    print("avg: ", average(diff))
    print("stdev: ", stdev(diff))

    children = (swedishChildrenList, israeliChildrenList)
    with open(picklepath(PICKLE_FILE), "wb") as pklfile:
        pkl.dump(children, pklfile)


# Tag Israeli children with found Swedish RF
def tagIsraeliWithSwedish(israeliChildrenList, swedishChildrenList):
    with open(randomforestpath(PICKLE_RANDOM_FOREST_FILE), "rb") as pklfile:
        rf_classifier = pkl.load(pklfile)

    predicted_ICT = []
    for c in israeliChildrenList:
        ict_val = rf_classifier.classifyIsrBySwe(c)
        c.regICT = ict_val
        predicted_ICT.append(ict_val)
    orig_ICT = [c.autoICT * MONTHS if c.autoICT != NA else c.autoICT for c in (israeliChildrenList)]
    print("Original tagging: ")
    print(orig_ICT)
    print("Predicted tagging: ")
    print(predicted_ICT)
    print("Differences in days: ")
    diff = [int((x-y)*30) for x, y in zip(orig_ICT, predicted_ICT) if x != NA and y != NA]
    print([diff.count(x) for x in range(-30, 30)])
    print("median: ", median(diff))
    print("avg: ", average(diff))
    print("stdev: ", stdev(diff))


def createFeatureHistogram(israeliChildrenList, swedishChildrenList):
    print("Feature NaN histogram:")
    isr_classi_f, X_classi_isr, c_classi_isr = getDataForBooleanClassification(israeliChildrenList)
    print(isr_classi_f)
    print([list(x).count(np.nan) for x in np.array(X_classi_isr).transpose()])
    swe_classi_f, X_classi_swe, c_classi_swe = getDataForBooleanClassification(swedishChildrenList)
    print(swe_classi_f)
    print([list(x).count(np.nan) for x in np.array(X_classi_swe).transpose()])