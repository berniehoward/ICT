from LearningStage.utility import exportTreesFromForest, removeNationFeature
from LearningStage.classificationExperiment import createBoolClassification,getDataForBooleanClassification
from LearningStage.regressionExperiment import createRegressionClassification, getDataForClassification
from LearningStage.utility import *
from Parser.auxiliary import *
import os
from Parser.auxiliary import MONTHS, NA
import pickle as pkl
from LearningStage.classifier import RegressionForestAlgorithm
from statistics import stdev
from numpy import average, median
from LearningStage.classificationRandomForest import booleanTreesExp, booleanTreesTuning, \
    booleanTreesFeatureSelectionAndFinalClassifier
from LearningStage.boolAdaBoost import booleanAdaExp, booleanAdaTuning, booleanAdaFeatureSelectionAndFinalClassifier
from LearningStage.regressionAdaBoost import regressionAdaExp, regressionAdaTuning, \
    regressionAdaFeatureSelectionAndFinalClassifier
from LearningStage.regressionRandomForest import regressionForestExp, regressionForestTuning, \
     regressionForestFeatureSelectionAndFinalClassifier
import numpy as np

# TODO - put the definitions in their own file
######################################## Definitions ##################################3

RF_hops = [1, 0.05, 1, 5]
# Boolean Random Forest:
isr_ranges = [range(56, 77), np.arange(0.1, 0.20, 0.05), range(19, 30), range(5, 10, 5)]
swe_ranges = [range(80, 101), np.arange(0.5, 1.05, 0.05), range(39, 60), range(15, 20, 5)]
mixed_ranges = [range(40, 61), np.arange(0.6, 0.65, 0.05), range(4, 10), range(5, 10, 5)]
isr_m_ranges = [range(47, 76), np.arange(0.15, 0.45, 0.05), range(1, 4), range(10, 45, 5)]
swe_m_ranges = [range(9, 30), np.arange(0.15, 1.05, 0.05), range(8, 29), range(5, 30, 5)]
mixed_m_ranges = [range(130, 151), np.arange(0.1, 0.25, 0.05), range(3, 9), range(35, 40, 5)]
isr_f_ranges = [range(163, 201), np.arange(0.35, 0.45, 0.05), range(2, 6), range(5, 10, 5)]
swe_f_ranges = [range(171, 201), np.arange(0.7, 1.05, 0.05), range(2, 6), range(5, 15, 5)]
mixed_f_ranges = [range(190, 201), np.arange(0.15, 0.2, 0.05), range(5, 8), range(10, 15, 5)]
BRF_PARM = isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
           swe_f_ranges, mixed_f_ranges, RF_hops

# Regression Random Forest:
isr_ranges = [range(128, 149), np.arange(0.1, 1.05, 0.05), range(20, 41), range(10, 30, 5)]
sw_ranges = [range(39, 60), np.arange(0.25, 0.95, 0.05), range(3, 17), range(15, 35, 5)]
mix_ranges = [range(56, 75), np.arange(0.25, 0.9, 0.05), range(3, 9), range(15, 45, 5)]
isr_m_ranges = [range(94, 114), range(0), range(12, 32), range(5, 20, 5)]
swe_m_ranges = [range(48, 68), range(0), range(5, 25), range(5, 30, 5)]
mixed_m_ranges = [range(83, 103), range(0), range(5, 25), range(5, 35, 5)]
isr_f_ranges = [range(80, 95), np.arange(0.1, 0.5, 0.05), range(0), range(5, 25, 5)]
swe_f_ranges = [range(31, 51), np.arange(0.2, 1, 0.05), range(6, 26), range(5, 20, 5)]
mixed_f_ranges = [range(79, 99), np.arange(0.25, 1, 0.05), range(5, 25), range(5, 25, 5)]
RRF_PARM = isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
           swe_f_ranges, mixed_f_ranges, RF_hops

# TODO - fill the rest of the parameters for AdaBoost
AB_hops = [1, 1, 0.05, 1, 5]
# Boolean AdaBoost:
isr_ranges = []
sw_ranges = []
mix_ranges = []
isr_m_ranges = []
swe_m_ranges = []
mixed_m_ranges = []
isr_f_ranges = []
swe_f_ranges = []
mixed_f_ranges = []
BAB_PARM = isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
           swe_f_ranges, mixed_f_ranges, AB_hops

# Regression AdaBoost:
isr_ranges = []
sw_ranges = []
mix_ranges = []
isr_m_ranges = []
swe_m_ranges = []
mixed_m_ranges = []
isr_f_ranges = []
swe_f_ranges = []
mixed_f_ranges = []
RAB_PARM = isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
           swe_f_ranges, mixed_f_ranges, AB_hops

#######################################################################################################################

# TODO - Does all the functions really belong to this file? or we need to move some? maybe file for RF general
# function and file to AdaBoost?


def randomForestExperiment(swedishChildrenList, israeliChildrenList, printMode=False):
    print("Boolean trees: ")
    isr_f, isr_classification_RF, swe_f, swe_classification_RF = \
    createBoolClassification(swedishChildrenList, israeliChildrenList, booleanTreesExp, booleanTreesTuning,
                             booleanTreesFeatureSelectionAndFinalClassifier, BRF_PARM)
    print("Regression trees: ")
    isr_f, isr_regression_RF, swe_f, swe_regression_RF = \
        createRegressionClassification(swedishChildrenList, israeliChildrenList, regressionForestExp,
                                       regressionForestTuning, regressionForestFeatureSelectionAndFinalClassifier,
                                       RRF_PARM)
    if printMode:
        exportTreesFromForest(isr_f, isr_regression_RF, Nationality.ISR.name, DecisionAlgorithmType.REGRESSION.name)
        exportTreesFromForest(swe_f, swe_regression_RF, Nationality.SWE.name, DecisionAlgorithmType.REGRESSION.name)
        exportTreesFromForest(isr_f, isr_classification_RF, Nationality.ISR.name, DecisionAlgorithmType.CLASSIFICATION.value)
        exportTreesFromForest(swe_f, swe_classification_RF, Nationality.SWE.name, DecisionAlgorithmType.CLASSIFICATION.value)


def adaBoostExperiment(swedishChildrenList, israeliChildrenList, printMode=False):
    # print("Boolean AdaBoost: ")
    # isr_f, isr_classification_AB, swe_f, swe_classification_AB = \
    #     createBoolClassification(swedishChildrenList, israeliChildrenList, booleanAdaExp, booleanAdaTuning,
    #                              booleanAdaFeatureSelectionAndFinalClassifier, BAB_PARM)
    print("Regression AdaBoost: ")
    isr_f, isr_regression_RF, swe_f, swe_regression_RF = \
        createRegressionClassification(swedishChildrenList, israeliChildrenList, regressionAdaExp, regressionAdaTuning,
                                       regressionAdaFeatureSelectionAndFinalClassifier, RAB_PARM)


# Perform experiment for the third stage
def program(swedishChildrenList, israeliChildrenList, printMode=False):
    printMode = True
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
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
    rf_classifier = RegressionForestAlgorithm(data, isr_class_args, isr_reg_args, swe_class_args, swe_reg_args)

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
    print([diff.count(x) for x in range(-30, 30)])
    print("median: ", median(diff))
    print("avg: ", average(diff))
    print("stdev: ", stdev(diff))

    children = (swedishChildrenList, israeliChildrenList)
    with open(picklepath(PICKLE_FILE), "wb") as pklfile:
        pkl.dump(children, pklfile)