from LearningStage.utility import getTenMostCommonAges, mergeChildren, splitByGender, removeNationFeature
from LearningStage.classificationRandomForest import *
from LearningStage.featureSelection import *
from LearningStage.RFclassifier import *
import numpy as np
import os
from Parser.auxiliary import Nationality, NA


# Boolean classification of israeli, swedish or mixed children
def createBoolClassification(swedishChildrenList, israeliChildrenList, expFunc, tuningFunc,
                             featureSelectionAndFinalClassifierFunc, PARM):
    # Get feature vectors and classification
    is_f, is_X, is_c = getDataForBooleanClassification(israeliChildrenList)
    is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
#
    sw_f, sw_X, sw_c = getDataForBooleanClassification(swedishChildrenList)
    # sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)

    # allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    # mix_f, mix_X, mix_c = getDataForBooleanClassification(allChildren)
    # mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(allChildren)

    # expFunc(is_f, is_X, is_c, "Israeli")
    # expFunc(sw_f, sw_X, sw_c, "Swedish")
    # expFunc(mix_f, mix_X, mix_c, "Mixed")

    # print("Males: ")
    # expFunc(is_m_f, is_m_X, is_m_c, "Israeli Males")
    # expFunc(sw_m_f, sw_m_X, sw_m_c, "Swedish Males")
    # expFunc(mix_m_f, mix_m_X, mix_m_c, "Mixed Males")

    # print("Females: ")
    # expFunc(is_f_f, is_f_X, is_f_c, "Israeli Females")
    # expFunc(sw_f_f, sw_f_X, sw_f_c, "Swedish Females")
    # expFunc(mix_f_f, mix_f_X, mix_f_c, "Mixed Females")

    # ####### LOCAL SEARCH ########
    # print("Local Search: ")
    # isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, \
    # swe_f_ranges, mixed_f_ranges = PARM
#
    # isr_params, isr_score = tuningFunc(is_f, is_X, is_c, randomForestCreator, isr_ranges)
    # print("Israeli: ", " params: ", isr_params, " score: ", 1 - isr_score)
    # swe_params, swe_score = tuningFunc(sw_f, sw_X, sw_c, randomForestCreator, swe_ranges)
    # print("Swedish: ", " params: ", swe_params, " score: ", 1 - swe_score)
    # mix_params, mix_score = tuningFunc(mix_f, mix_X, mix_c, randomForestCreator, mixed_ranges)
    # print("Mix: ", " params: ", mix_params, " score: ", 1 - mix_score)
#
    # ####### LOCAL SEARCH - Divided to MALES AND FEMALES ########
    # print("Local Search, Males: ")
    # isr_params, isr_score = tuningFunc(is_m_f, is_m_X, is_m_c, randomForestCreator, isr_m_ranges)
    # print("Israeli Males: ", " params: ", isr_params, " score: ", 1 - isr_score)
    # swe_params, swe_score = tuningFunc(sw_m_f, sw_m_X, sw_m_c, randomForestCreator, swe_m_ranges)
    # print("Swedish Males: ", " params: ", swe_params, " score: ", 1 - swe_score)
    # mix_params, mix_score = tuningFunc(mix_m_f, mix_m_X, mix_m_c, randomForestCreator, mixed_m_ranges)
    # print("Mixed Males: ", " params: ", mix_params, " score: ", 1 - mix_score)
#
    # print("Local Search, Females: ")
    # isr_params, isr_score = tuningFunc(is_f_f, is_f_X, is_f_c, randomForestCreator, isr_f_ranges)
    # print("Israeli Females: ", " params: ", isr_params, " score: ", 1 - isr_score)
    # swe_params, swe_score = tuningFunc(sw_f_f, sw_f_X, sw_f_c, randomForestCreator, swe_f_ranges)
    # print("Swedish Females: ", " params: ", swe_params, " score: ", 1 - swe_score)
    # mix_params, mix_score = tuningFunc(mix_f_f, mix_f_X, mix_f_c, randomForestCreator, mixed_f_ranges)
    # print("Mixed Females: ", " params: ", mix_params, " score: ", 1 - mix_score)
#
    return featureSelectionAndFinalClassifierFunc(is_X, is_f, is_c, sw_X, sw_f, sw_c)




