from LearningStage.utility import getTenMostCommonAges, mergeChildren, splitByGender, removeNationFeature
from Parser.auxiliary import NA
from LearningStage.booleanRandomForest import *
import numpy as np
import os
from Parser.auxiliary import Nationality
from LearningStage.featureSelection import *


# Boolean classification of israeli, swedish or mixed children
def createBoolClassification(swedishChildrenList, israeliChildrenList):
    # Get feature vectors and classification
    is_f, is_X, is_c = getDataForBooleanClassification(israeliChildrenList)
    # is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)

    sw_f, sw_X, sw_c = getDataForBooleanClassification(swedishChildrenList)
    # sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)

    # allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    # mix_f, mix_X, mix_c = getDataForBooleanClassification(allChildren)
    # mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(allChildren)

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

    ######## LOCAL SEARCH ########
    # print("Local Search: ")
    # isr_ranges = [range(56,77), np.arange(0.1, 0.20, 0.05), range(19, 30), range(5, 10, 5)]
    # swe_ranges = [range(80,101), np.arange(0.5, 1.05, 0.05), range(39, 60), range(15, 20, 5)]
    # mixed_ranges = [range(40,61), np.arange(0.6, 0.65, 0.05), range(4, 10), range(5, 10, 5)]

    # isr_params, isr_score = booleanParametersTuning(is_f, is_X, is_c, randomForestCreator, isr_ranges)
    # print("Israeli: ", " params: ", isr_params, " score: ", 1 - isr_score)
    # swe_params, swe_score = booleanParametersTuning(sw_f, sw_X, sw_c, randomForestCreator, swe_ranges)
    # print("Swedish: ", " params: ", swe_params, " score: ", 1 - swe_score)
    # mix_params, mix_score = booleanParametersTuning(mix_f, mix_X, mix_c, randomForestCreator, mixed_ranges)
    # print("Mix: ", " params: ", mix_params, " score: ", 1 - mix_score)

    ######## LOCAL SEARCH - Divided to MALES AND FEMALES ########
    # print("Local Search, Males: ")
    # isr_m_ranges = [range(47, 76), np.arange(0.15, 0.45, 0.05), range(1, 4), range(10, 45, 5)]
    # swe_m_ranges = [range(9, 30), np.arange(0.15, 1.05, 0.05), range(8, 29), range(5, 30, 5)]
    # mixed_m_ranges = [range(130, 151), np.arange(0.1, 0.25, 0.05), range(3, 9), range(35, 40, 5)]

    # isr_params, isr_score = booleanParametersTuning(is_m_f, is_m_X, is_m_c, randomForestCreator, isr_m_ranges)
    # print("Israeli Males: ", " params: ", isr_params, " score: ", 1 - isr_score)
    # swe_params, swe_score = booleanParametersTuning(sw_m_f, sw_m_X, sw_m_c, randomForestCreator, swe_m_ranges)
    # print("Swedish Males: ", " params: ", swe_params, " score: ", 1 - swe_score)
    # mix_params, mix_score = booleanParametersTuning(mix_m_f, mix_m_X, mix_m_c, randomForestCreator, mixed_m_ranges)
    # print("Mixed Males: ", " params: ", mix_params, " score: ", 1 - mix_score)

    # print("Local Search, Females: ")
    # isr_f_ranges = [range(163, 201), np.arange(0.35, 0.45, 0.05), range(2, 6), range(5, 10, 5)]
    # swe_f_ranges = [range(171, 201), np.arange(0.7, 1.05, 0.05), range(2, 6), range(5, 15, 5)]
    # mixed_f_ranges = [range(190, 201), np.arange(0.15, 0.2, 0.05), range(5, 8), range(10, 15, 5)]

    # isr_params, isr_score = booleanParametersTuning(is_f_f, is_f_X, is_f_c, randomForestCreator, isr_f_ranges)
    # print("Israeli Females: ", " params: ", isr_params, " score: ", 1 - isr_score)
    # swe_params, swe_score = booleanParametersTuning(sw_f_f, sw_f_X, sw_f_c, randomForestCreator, swe_f_ranges)
    # print("Swedish Females: ", " params: ", swe_params, " score: ", 1 - swe_score)
    # mix_params, mix_score = booleanParametersTuning(mix_f_f, mix_f_X, mix_f_c, randomForestCreator, mixed_f_ranges)
    # print("Mixed Females: ", " params: ", mix_params, " score: ", 1 - mix_score)

    # Best chosen forests
    isr_forest = RandomForestClassifier(max_depth=20, max_features=0.1, random_state=1,
                                    min_samples_leaf=5, n_estimators=57)
    swe_forest = RandomForestClassifier(max_depth=42, max_features=0.55, random_state=1,
                                    min_samples_leaf=15, n_estimators=84)

    # Feature selection:
    print("Feature selection: ")
    imputer = Imputer(strategy='median', axis=0)

    is_X, f = removeNationFeature(is_X, is_f)
    is_X = imputer.fit_transform(is_X)
    # performSelectKBestFeatures(is_X, is_c, isr_forest, Nationality.ISR.name)

    sw_X, f = removeNationFeature(sw_X, sw_f)
    sw_X = imputer.fit_transform(sw_X)
    # performSelectKBestFeatures(sw_X, sw_c, swe_forest, Nationality.SWE.name)


    # performRFE(is_X, is_c, isr_forest, Nationality.ISR.name)
    # performRFE(sw_X, sw_c, swe_forest, Nationality.SWE.name)

    # create final regression forest :
    is_k = 26 #14
    sw_k = 11 #12
#
    # isr_f, isr_final_RF = createFinalClassificationForest(is_X, is_c, is_f, is_k, isr_forest, True)
    # swe_f, swe_final_RF = createFinalClassificationForest(sw_X, sw_c, sw_f, sw_k, swe_forest, True)
    # return isr_f, isr_final_RF, swe_f, swe_final_RF


