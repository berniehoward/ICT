from LearningStage.utility import getTenMostCommonAges, mergeChildren, splitByGender
from Parser.auxiliary import NA
from LearningStage.regressionRandomForest import *
from LearningStage.booleanRandomForest import *
import numpy as np
import os


# Return features(list of all the features' names) , data(list of all the features) and
# classifications (list of boolean tags - the child has ICT or not)
def getDataForBooleanClassification(children):
    data = []
    classifications = []
    features = []
    common_ages = sorted(getTenMostCommonAges(children, 8))
    for ch in children:
        if len(ch.goodSamples) == 0:
            continue
        f, d, c = ch.generateParametersForRegressionDecisionTree(common_ages, False)
        features = [i for i in f]
        c = 1 if c != 0 else 0
        data.append([x if x != NA else np.NaN for x in d])
        classifications.append(c)
    return features, data, classifications


# Return features(list of all the features' names) , data(list of all the features) and
# classifications (list of ICT tags for every child)
def getDataForClassification(children):
    data = []
    classifications = []
    features = []
    common_ages = sorted(getTenMostCommonAges(children, 8))
    for ch in children:
        if len(ch.goodSamples) == 0:
            continue
        f, d, c = ch.generateParametersForRegressionDecisionTree(common_ages, False)
        features = [i for i in f]
        if not c:
            continue
        data.append([x if x != NA else np.NaN for x in d])
        classifications.append(c)
    return features, data, classifications


# Return data and classification separated by gender:
def seperateGenders(children):
    males, females = splitByGender(children)
    m_f, m_X, m_c = getDataForClassification(males)
    f_f, f_X, f_c = getDataForClassification(females)
    return m_f, m_X, m_c, f_f, f_X, f_c


# Print information about all the parameters in order to determine the wanted ranges
def determineRanges(f, X, c, function):

    # Parameters: n_est, max_features, max_depth, min_samples_leaf, min_samples_split
    ranges = [range(1, 201), np.arange(0.1, 1.05, 0.05), range(1, 90), range(5, 100, 5), range(10, 200, 10)]
    default_parameters = [10, "auto", None, 1, 2]
    headers = ["Number of trees:", "Percentage of features:", "Max depth:", "Min samples in leaf:", "Min samples to split:"]

    for r in range(0, len(ranges)):
        for i in ranges[r]:
            args = default_parameters
            args[r] = i
            r_forest, score = function(f, X, c, args)
            print(headers[r], " %.2f, MSE: %.3f" % (i, abs(score)))


def createRegressionClassification(swedishChildrenList, israeliChildrenList):
    # Get feature vectors and classification
    is_f, is_X, is_c = getDataForClassification(israeliChildrenList)
    sw_f, sw_X, sw_c = getDataForClassification(swedishChildrenList)
    allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    mix_f, mix_X, mix_c = getDataForClassification(allChildren)
    is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
    sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)
    mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(allChildren)

    print("Regression trees: ")
    print("Mix genders: ")
    regressionTreesExp(is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, "mix")
    print("Males: ")
    regressionTreesExp(is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, mix_m_f, mix_m_X, mix_m_c, "M")
    print("Females: ")
    regressionTreesExp(is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c, "F")


def createBoolClassification(swedishChildrenList, israeliChildrenList):
    # Get feature vectors and classification
    is_f, is_X, is_c = getDataForBooleanClassification(israeliChildrenList)
    printVectors(is_f, is_X)
    # sw_f, sw_X, sw_c = getDataForBooleanClassification(swedishChildrenList)
    # allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    # mix_f, mix_X, mix_c = getDataForBooleanClassification(allChildren)
    # is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
    # sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)
    # mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(swedishChildrenList)

    print("Boolean trees: ")
    print("Mix genders: ")
    # booleanTreesExp(is_f, is_X, is_c, "Israeli")
    # booleanTreesExp(sw_f, sw_X, sw_c, "Swedish")
    # booleanTreesExp(mix_f, mix_X, mix_c, "Mixed")

    # print("Males: ")
    # booleanTreesExp(is_m_f, is_m_X, is_m_c, "Israeli Males")
    # booleanTreesExp(sw_m_f, sw_m_X, sw_m_c, "Swedish  Males")
    # booleanTreesExp(mix_m_f, mix_m_X, mix_m_c, "Mixed  Males")

    # print("Females: ")
    # booleanTreesExp(is_f_f, is_f_X, is_f_c, "Israeli Females")
    # booleanTreesExp(sw_f_f, sw_f_X, sw_f_c, "Swedish  Females")
    # booleanTreesExp(mix_f_f, mix_f_X, mix_f_c, "Mixed  Females")


# Perform the experiment of the third stage
def program(swedishChildrenList, israeliChildrenList):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    createBoolClassification(swedishChildrenList, israeliChildrenList)
    # createRegressionClassification(swedishChildrenList, israeliChildrenList)