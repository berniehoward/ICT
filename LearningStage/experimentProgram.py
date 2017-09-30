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


# Perform experiment for the "random forest" third stage
def program(swedishChildrenList, israeliChildrenList, printMode=False):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    #isr_f, isr_classification_RF, swe_f, swe_classification_RF = \
    createBoolClassification(swedishChildrenList, israeliChildrenList)
    isr_f, isr_regression_RF, swe_f, swe_regression_RF = \
        createRegressionClassification(swedishChildrenList, israeliChildrenList)
    #if printMode:
    #    exportTreesFromForest(isr_f, isr_regression_RF, "Israeli")
    #    exportTreesFromForest(swe_f, swe_regression_RF, "Swedish")
	#    exportTreesFromForest(isr_f, isr_classification_RF, Nationality.ISR.name, TreeType.CLASSIFICATION.value)
    #    exportTreesFromForest(swe_f, swe_classification_RF, Nationality.SWE.name, TreeType.CLASSIFICATION.value)


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
def tagChildren(israeliChildrenList, swedishChildrenList):
    with open(randomforestpath(PICKLE_RANDOM_FOREST_FILE), "rb") as pklfile:
        rf_classifier = pkl.load(pklfile)

    orig_ICT = []
    predicted_ICT = []
    for c in israeliChildrenList + swedishChildrenList:
        ict_val = rf_classifier.classifyChild(c)
        c.regICT = ict_val
        predicted_ICT.append(ict_val)
        #predicted_ICT.append((rf_classifier.classifyChild(c), c))
    #sorted_predicted_ICT = sorted(predicted_ICT, key=lambda tup: tup[0])
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