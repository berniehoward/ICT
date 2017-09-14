from LearningStage.utility import getTenMostCommonAges, mergeChildren, splitByGender
from Parser.auxiliary import NA
from LearningStage.regressionRandomForest import *
from LearningStage.booleanRandomForest import *
import numpy as np
import os

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

def createRegressionClassification(swedishChildrenList, israeliChildrenList):
    # is_f, is_X, is_c = getDataForClassification(israeliChildrenList)
    # sw_f, sw_X, sw_c = getDataForClassification(swedishChildrenList)
    # allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    # mix_f, mix_X, mix_c = getDataForClassification(allChildren)
    is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
    sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)
    mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(swedishChildrenList)

    # Regression trees:
    print("Regression trees: ")
    print("Mix genders: ")
    # regressionTreesExp(is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, "mix")
    print("Males: ")
    regressionTreesExp(is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, mix_m_f, mix_m_X, mix_m_c, "M")
    print("Females: ")
    regressionTreesExp(is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c, "F")

def createBoolClassification(swedishChildrenList, israeliChildrenList):
    is_f, is_X, is_c = getDataForBooleanClassification(israeliChildrenList)
    printVectors(is_f, is_X)
    # sw_f, sw_X, sw_c = getDataForBooleanClassification(swedishChildrenList)
    # allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    # mix_f, mix_X, mix_c = getDataForBooleanClassification(allChildren)
    # is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
    # sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)
    # mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(swedishChildrenList)

    # Boolean trees:
    print("Boolean trees: ")
    print("Mix genders: ")
    # booleanTreesExp(is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, "mix")
    # print("Males: ")
    # booleanTreesExp(is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, mix_m_f, mix_m_X, mix_m_c, "M")
    # print("Females: ")
    # booleanTreesExp(is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c, "F")

# Perform the experiment of the third stage
def program(swedishChildrenList, israeliChildrenList):
    # Get feature vectors and classification
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    createBoolClassification(swedishChildrenList, israeliChildrenList)
    #createRegressionClassification(swedishChildrenList, israeliChildrenList)