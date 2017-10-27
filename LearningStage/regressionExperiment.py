
from LearningStage.regressionRandomForest import *
from Parser.auxiliary import Nationality
from LearningStage.utility import *


# Regression classificator of israeli, swedish or mixed children
def createRegressionClassification(swedishChildrenList, israeliChildrenList, expFunc, tuningFunc,
                                   finalClassifierFunc, params, classifiers, ks):
    # Get feature vectors and classification
    imputer = Imputer(strategy='median', axis=0)
    is_f, is_X, is_c = getDataForClassification(israeliChildrenList)
    is_X = imputer.fit_transform(is_X)
    # sw_f, sw_X, sw_c = getDataForClassification(swedishChildrenList)
    # sw_X = imputer.fit_transform(sw_X)
    # allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    # mix_f, mix_X, mix_c = getDataForClassification(allChildren)
    # mix_X = imputer.fit_transform(mix_X)
    # is_m_f, is_m_X, is_m_c, is_f_f, is_f_X, is_f_c = seperateGenders(israeliChildrenList)
    # sw_m_f, sw_m_X, sw_m_c, sw_f_f, sw_f_X, sw_f_c = seperateGenders(swedishChildrenList)
    # mix_m_f, mix_m_X, mix_m_c, mix_f_f, mix_f_X, mix_f_c = seperateGenders(allChildren)

    # Determinate ranges:
    # print("Both Genders: ")
    # expFunc(is_f, is_X, is_c, "Israeli")
    # expFunc(sw_f, sw_X, sw_c, "Swedish")
    # expFunc(mix_f, mix_X, mix_c, "Mixed")
#
    # print("Males: ")
    # expFunc(is_m_f, is_m_X, is_m_c, "Israeli Males")
    # expFunc(sw_m_f, sw_m_X, sw_m_c, "Swedish Males")
    # expFunc(mix_m_f, mix_m_X, mix_m_c, "Mixed Males")
#
    # print("Females: ")
    # expFunc(is_f_f, is_f_X, is_f_c, "Israeli Females")
    # expFunc(sw_f_f, sw_f_X, sw_f_c, "Swedish Females")
    # expFunc(mix_f_f, mix_f_X, mix_f_c, "Mixed Females")

    # Local search:
    # vectors = is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, \
    #           mix_m_f, mix_m_X, mix_m_c, is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c
    # tuningFunc(params, vectors)

    # Feature selection:
    isr_class, swe_class = classifiers
    is_X, f = removeNationFeature(is_X, is_f)
    is_X, f = removeIsraeliBadFeatures(is_X, f)
    is_X = imputer.fit_transform(is_X)
    performSelectKBestFeatures(is_X, is_c, isr_class, Nationality.ISR.name)
    # performSelectKBestFeatures(sw_X, sw_c, swe_class, Nationality.SWE.name)
    performRFE(is_X, is_c, isr_class, Nationality.ISR.name)
    # performRFE(sw_X, sw_c, swe_class, Nationality.SWE.name)

    # create final regression classifier:
    is_k, sw_k = ks
    # return finalClassifierFunc(is_X, is_c, is_f, is_k, sw_X, sw_c, sw_f, sw_k, classifiers)

