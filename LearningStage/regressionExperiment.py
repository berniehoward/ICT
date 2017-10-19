from LearningStage.featureSelection import *
from LearningStage.regressionRandomForest import *
from sklearn.ensemble import RandomForestRegressor
from Parser.auxiliary import Nationality
from LearningStage.utility import mergeChildren
from LearningStage.regressionRandomForest import regressionTreesExp


# Regression classificator of israeli, swedish or mixed children
def createRegressionClassification(swedishChildrenList, israeliChildrenList, expFunc, tuningFunc,
                                   featureSelectionAndFinalClassifierFunc, params):
    # Get feature vectors and classification
    imputer = Imputer(strategy='median', axis=0)
    is_f, is_X, is_c = getDataForClassification(israeliChildrenList)
    is_X = imputer.fit_transform(is_X)
    sw_f, sw_X, sw_c = getDataForClassification(swedishChildrenList)
    sw_X = imputer.fit_transform(sw_X)
    allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    mix_f, mix_X, mix_c = getDataForClassification(allChildren)
    mix_X = imputer.fit_transform(mix_X)
    is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
    sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)
    mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(allChildren)

    # Determinate ranges:
    print("Bout Genders: ")
    expFunc(is_f, is_X, is_c, "Israeli")
    expFunc(sw_f, sw_X, sw_c, "Swedish")
    expFunc(mix_f, mix_X, mix_c, "Mixed")

    print("Males: ")
    expFunc(is_m_f, is_m_X, is_m_c, "Israeli Males")
    expFunc(sw_m_f, sw_m_X, sw_m_c, "Swedish Males")
    expFunc(mix_m_f, mix_m_X, mix_m_c, "Mixed Males")

    print("Females: ")
    expFunc(is_f_f, is_f_X, is_f_c, "Israeli Females")
    expFunc(sw_f_f, sw_f_X, sw_f_c, "Swedish Females")
    expFunc(mix_f_f, mix_f_X, mix_f_c, "Mixed Females")

    # Local search:
    vectors = is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, \
              mix_m_f, mix_m_X, mix_m_c, is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c
    tuningFunc(params, vectors)

    # TODO - until here generic, after it only suits to RF

    # isr_forest = RandomForestRegressor(max_depth=20, max_features=0.8, random_state=1, min_samples_split=2,
    #                                    min_samples_leaf=10, n_estimators=143)
    # swe_forest = RandomForestRegressor(max_depth=16, max_features=0.85, random_state=1, min_samples_split=2,
    #                                    min_samples_leaf=30, n_estimators=45)
    #
    # # Feature selection:
    # performSelectKBestFeatures(is_X, is_c, isr_forest, Nationality.ISR.name)
    # performSelectKBestFeatures(sw_X, sw_c, swe_forest, Nationality.SWE.name)
    # performRFE(is_X, is_c, isr_forest, Nationality.ISR.name)
    # performRFE(sw_X, sw_c, swe_forest, Nationality.SWE.name)
    # is_k = 17
    # sw_k = 13
    #
    # # create final regression forest :
    # is_f, is_final_RF = createFinalRegressionForest(is_X, is_c, is_f, is_k, isr_forest, True)
    # sw_f, sw_final_RF = createFinalRegressionForest(sw_X, sw_c, sw_f, sw_k, swe_forest, True)
    # return is_f, is_final_RF, sw_f, sw_final_RF
