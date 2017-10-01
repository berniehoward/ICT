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


# TODO - what is this function? we need to delete it? there is same function in this name at the file classificationExp
# Boolean classification of israeli, swedish or mixed children
def createBoolClassification(swedishChildrenList, israeliChildrenList, expFunc, ParametersTuningFunc, BRF_PARM):
    # Get feature vectors and classification
    is_f, is_X, is_c = getDataForBooleanClassification(israeliChildrenList)
    sw_f, sw_X, sw_c = getDataForBooleanClassification(swedishChildrenList)
    allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    mix_f, mix_X, mix_c = getDataForBooleanClassification(allChildren)
    is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
    sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)
    mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(swedishChildrenList)

    print("Boolean trees: ")
    expFunc(is_f, is_X, is_c, "Israeli")
    expFunc(sw_f, sw_X, sw_c, "Swedish")
    expFunc(mix_f, mix_X, mix_c, "Mixed")

    print("Males: ")
    expFunc(is_m_f, is_m_X, is_m_c, "Israeli Males")
    expFunc(sw_m_f, sw_m_X, sw_m_c, "Swedish  Males")
    expFunc(mix_m_f, mix_m_X, mix_m_c, "Mixed  Males")

    print("Females: ")
    expFunc(is_f_f, is_f_X, is_f_c, "Israeli Females")
    expFunc(sw_f_f, sw_f_X, sw_f_c, "Swedish  Females")
    expFunc(mix_f_f, mix_f_X, mix_f_c, "Mixed  Females")

    isr_ranges, swe_ranges, mixed_ranges, hops = BRF_PARM
    isr_params, isr_score = ParametersTuningFunc(is_f, is_X, is_c, randomForestCreator, isr_ranges, hops)
    print("Israeli: ", " params: ", isr_params, " score: ", isr_score)
    swe_params, swe_score = ParametersTuningFunc(sw_f, sw_X, sw_c, randomForestCreator, swe_ranges, hops)
    print("Swedish: ", " params: ", swe_params, " score: ", swe_score)
    mix_params, mix_score = ParametersTuningFunc(mix_f, mix_X, mix_c, randomForestCreator, mixed_ranges, hops)
    print("Mix: ", " params: ", mix_params, " score: ", mix_score)