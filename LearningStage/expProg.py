from LearningStage.utility import getTenMostCommonAges, mergeChildren, splitByGender
from Parser.auxiliary import NA
from LearningStage.regressionRandomForest import regressionTreesExp
from LearningStage.booleanClassificationFunctions import createBoolClassification
import numpy as np
import os
from LearningStage.featureSelection import *
from sklearn.ensemble import RandomForestRegressor
from Parser.auxiliary import Nationality

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


# Regression classificator of israeli, swedish or mixed children
def createRegressionClassification(swedishChildrenList, israeliChildrenList):
    # Get feature vectors and classification
    imputer = Imputer(strategy='median', axis=0)
    is_f, is_X, is_c = getDataForClassification(israeliChildrenList)
    is_X = imputer.fit_transform(is_X)
    sw_f, sw_X, sw_c = getDataForClassification(swedishChildrenList)
    sw_X = imputer.fit_transform(sw_X)
    # allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    # mix_f, mix_X, mix_c = getDataForClassification(allChildren)
    # mix_X = imputer.fit_transform(mix_X)
    #
    # is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
    # sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)
    # mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(allChildren)
    #
    # print("Regression trees: ")
    # print("Mix genders: ")
    # regressionTreesExp(is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, "mix")
    # print("Males: ")
    # regressionTreesExp(is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, mix_m_f, mix_m_X, mix_m_c, "M")
    # print("Females: ")
    # regressionTreesExp(is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c, "F")

    isr_forest = RandomForestRegressor(max_depth=20, max_features=0.8, random_state=1, min_samples_split=2,
                                      min_samples_leaf=10, n_estimators=143)
    swe_forest = RandomForestRegressor(max_depth=16, max_features=0.85, random_state=1, min_samples_split=2,
                                      min_samples_leaf=30, n_estimators=45)

    # Feature selection:
    performSelectKBestFeatures(is_X, is_c, isr_forest, Nationality.ISR.name)
    performSelectKBestFeatures(sw_X, sw_c, swe_forest, Nationality.SWE.name)
    performRFE(is_X, is_c, isr_forest, Nationality.ISR.name)
    performRFE(sw_X, sw_c, swe_forest, Nationality.SWE.name)


# Perform the experiment of the third stage
def program(swedishChildrenList, israeliChildrenList):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    createBoolClassification(swedishChildrenList, israeliChildrenList)
    # createRegressionClassification(swedishChildrenList, israeliChildrenList)