from LearningStage.utility import exportTreesFromForest, removeNationFeature
from LearningStage.classificationExperiment import createBoolClassification,getDataForBooleanClassification
from LearningStage.regressionExperiment import createRegressionClassification, getDataForClassification
from LearningStage.utility import exportTreesFromForest, TreeType
from Parser.auxiliary import Nationality
import os
from Parser.auxiliary import MONTHS, NA
from LearningStage.classifier import RegressionForestAlgorithm
from statistics import stdev
from numpy import average, median

# Perform the experiment of the third stage
def program(swedishChildrenList, israeliChildrenList, printMode=False):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    #isr_f, isr_classification_RF, swe_f, swe_classification_RF = \
    createBoolClassification(swedishChildrenList, israeliChildrenList)
    isr_f, isr_regression_RF, swe_f, swe_regression_RF = createRegressionClassification(swedishChildrenList, israeliChildrenList)
    #if printMode:
    #    exportTreesFromForest(isr_f, isr_regression_RF, "Israeli")
    #    exportTreesFromForest(swe_f, swe_regression_RF, "Swedish")


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
    predicted_ICT = []
    for c in israeliChildrenList + swedishChildrenList:
        predicted_ICT.append(rf_classifier.classifyChild(c))
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

    # TODO - what is this part?  we need to move it to the function "program"
    """
    isr_f, isr_classification_RF, swe_f, swe_classification_RF =\
        createBoolClassification(swedishChildrenList, israeliChildrenList)
    # isr_f, isr_regression_RF, swe_f, swe_regression_RF = \
    #     createRegressionClassification(swedishChildrenList, israeliChildrenList)
    if printMode:
        # exportTreesFromForest(isr_f, isr_regression_RF, Nationality.ISR.value, TreeType.REGRESSION.value)
        # exportTreesFromForest(swe_f, swe_regression_RF, Nationality.SWE.value, TreeType.REGRESSION.value)
        exportTreesFromForest(isr_f, isr_classification_RF, Nationality.ISR.name, TreeType.CLASSIFICATION.value)
        exportTreesFromForest(swe_f, swe_classification_RF, Nationality.SWE.name, TreeType.CLASSIFICATION.value)

    """