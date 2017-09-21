from LearningStage.utility import getTenMostCommonAges, mergeChildren, splitByGender
from Parser.auxiliary import NA
from LearningStage.booleanRandomForest import *
import numpy as np
import os
from LearningStage.featureSelection import *


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


# Boolean classification of israeli, swedish or mixed children
def createBoolClassification(swedishChildrenList, israeliChildrenList):
    # Get feature vectors and classification
    is_f, is_X, is_c = getDataForBooleanClassification(israeliChildrenList)
    sw_f, sw_X, sw_c = getDataForBooleanClassification(swedishChildrenList)
    allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    mix_f, mix_X, mix_c = getDataForBooleanClassification(allChildren)
    # is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
    # sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)
    # mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(swedishChildrenList)

    print("Boolean trees: ")
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

    isr_ranges = [range(56, 77), np.arange(0.1, 0.20, 0.05), range(19, 30), range(5, 10, 5)]
    swe_ranges = [range(80, 101), np.arange(0.5, 1.05, 0.05), range(39, 60), range(15, 20, 5)]
    mixed_ranges = [range(40, 61), np.arange(0.6, 0.65, 0.05), range(4, 10), range(5, 10, 5)]
    hops = [1, 0.05, 1, 5]
    isr_params, isr_score = booleanParametersTuning(is_f, is_X, is_c, randomForestCreator, isr_ranges, hops)
    print("Israeli: ", " params: ", isr_params, " score: ", isr_score)
    # swe_params, swe_score = booleanParametersTuning(sw_f, sw_X, sw_c, randomForestCreator, swe_ranges, hops)
    # print("Swedish: ", " params: ", swe_params, " score: ", swe_score)
    # mix_params, mix_score = booleanParametersTuning(mix_f, mix_X, mix_c, randomForestCreator, mixed_ranges, hops)
    # print("Mix: ", " params: ", mix_params, " score: ", mix_score)