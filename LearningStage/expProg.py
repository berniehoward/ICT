from LearningStage.utility import getTenMostCommonAges, mergeChildren, splitByGender
from Parser.auxiliary import NA
from LearningStage.regressionRandomForest import regressionTreesExp
from LearningStage.booleanRandomForest import *
import numpy as np
import os
from LearningStage.featureSelection import *
from sklearn.ensemble import RandomForestRegressor


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


# Regression classificator of israeli, swedish or mixed children
def createRegressionClassification(swedishChildrenList, israeliChildrenList):
    # Get feature vectors and classification
    is_f, is_X, is_c = getDataForClassification(israeliChildrenList)
    sw_f, sw_X, sw_c = getDataForClassification(swedishChildrenList)
    allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    mix_f, mix_X, mix_c = getDataForClassification(allChildren)
    # is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
    # sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)
    # mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(allChildren)

    # print("Regression trees: ")
    # print("Mix genders: ")
    # regressionTreesExp(is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, "mix")
    # print("Males: ")
    # regressionTreesExp(is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, mix_m_f, mix_m_X, mix_m_c, "M")
    # print("Females: ")
    # regressionTreesExp(is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c, "F")
    is_forest = RandomForestRegressor(max_depth=20, max_features=0.8, random_state=1, min_samples_split=2,
                                      min_samples_leaf=10, n_estimators=143)
    sw_forest = RandomForestRegressor(max_depth=16, max_features=0.85, random_state=1, min_samples_split=2,
                                      min_samples_leaf=30, n_estimators=45)
    # print("selectKBestFeatures: ")
    # print("Israeli: ")
    # best_X, best_k, min_score = selectKBestFeatures(is_X, is_c, is_forest, "f_regression: ")
    # print("k: ", best_k, "mse: ", min_score)
    # best_X, best_k, min_score = selectKBestFeatures(is_X, is_c, is_forest, "scoring function: ", scoringIsraeliRegressorFunction)
    # print("k: ", best_k, "mse: ", min_score)
    print("Swedish: ")
    best_X, best_k, min_score = selectKBestFeatures(sw_X, sw_c, sw_forest, "f_regression: ")
    print("k: ", best_k, "mse: ", min_score)
    best_X, best_k, min_score = selectKBestFeatures(sw_X, sw_c, sw_forest, "scoring function: ", scoringSwedishRegressorFunction)
    print("k: ", best_k, "mse: ", min_score)


# Boolean classification of israeli, swedish or mixed children
def createBoolClassification(swedishChildrenList, israeliChildrenList):
    # Get feature vectors and classification
    # is_f, is_X, is_c = getDataForBooleanClassification(israeliChildrenList)
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
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    # createBoolClassification(swedishChildrenList, israeliChildrenList)
    createRegressionClassification(swedishChildrenList, israeliChildrenList)