from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier

from Parser.auxiliary import Nationality
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import numpy as np
from LearningStage.utility import removeIsraeliBadFeatures, removeSwedishBadFeatures
from sklearn.feature_selection import RFE
from LearningStage.utility import *
import pickle as pkl
from LearningStage.regressionRandomForest import getDataForClassification


# Return list of features lists organized by the age we get each feature
def divideToFeaturesGroups(nationality, X, f):
    features_groups = []
    if nationality == Nationality.ISR:
        X, f = removeIsraeliBadFeatures(X, f)
        features = [['sex', 'birthWeight (KG)', 'birthHeight (M)', 'gestationalAge (Weeks)', 'birthMonth',
                     'preterm flag', 'Height at 0.0', 'Weight at 0.0', 'BMI at 0.0',  'HC at 0.0', 'birthPosition',
                     'birthYear',  'nation'], ['Height at 0.1', 'Weight at 0.1', 'BMI at 0.1', 'WHO wfa z-score at 0.1',
                     'WHO wfl z-score at age 0.1', 'WHO lfa z-score at age 0.1', 'WHO hcfa z-score at 0.1', 'HC at 0.1',
                     'WHO wfa z-score at 0.1', 'WHO wfl z-score at age 0.1', 'WHO lfa z-score at age 0.1',
                     'WHO hcfa z-score at 0.1'],
                    ['Height at 0.2', 'Weight at 0.2', 'BMI at 0.2', 'WHO wfa z-score at 0.2',
                     'WHO wfl z-score at age 0.2', 'WHO lfa z-score at age 0.2', 'WHO hcfa z-score at 0.2', 'HC at 0.2',
                     'WHO wfa z-score at 0.2', 'WHO wfl z-score at age 0.2', 'WHO lfa z-score at age 0.2',
                     'WHO hcfa z-score at 0.2'], ['Height at 0.3', 'Weight at 0.3', 'BMI at 0.3',
                     'WHO wfa z-score at 0.3', 'WHO wfl z-score at age 0.3', 'WHO lfa z-score at age 0.3',
                     'WHO hcfa z-score at 0.3', 'HC at 0.3', 'WHO wfa z-score at 0.3', 'WHO wfl z-score at age 0.3',
                     'WHO lfa z-score at age 0.3',  'WHO hcfa z-score at 0.3'], ['Height at 0.4', 'Weight at 0.4',
                     'BMI at 0.4', 'WHO wfa z-score at 0.4', 'WHO wfl z-score at age 0.4', 'WHO lfa z-score at age 0.4',
                     'HC at 0.4', 'WHO wfa z-score at 0.4', 'WHO wfl z-score at age 0.4', 'WHO lfa z-score at age 0.4',
                     'WHO hcfa z-score at 0.4'], ['Height at 6 months (m)', 'Weight at 6 months (KG)',
                     "Height at 6 months (m) Avg'd", "Weight at 6 months (KG) Avg'd", 'Weight at 0.5', 'BMI at 0.5',
                     'WHO wfa z-score at 0.5', 'WHO wfl z-score at age 0.5', 'WHO lfa z-score at age 0.5',
                     'WHO hcfa z-score at 0.5', 'HC at 0.5',  "HC at 6 months Avg'd", 'Avg brothers HC at 6 months (m)',
                     'Avg brothers Height at 6 months (m)', 'Avg brothers Weight at 6 months (m)',
                     'WHO wfa z-score at 0.5', 'WHO wfl z-score at age 0.5', 'WHO lfa z-score at age 0.5',
                     'WHO hcfa z-score at 0.5'], ['Height at 1.0', 'Weight at 1.0', 'BMI at 1.0',
                     'WHO wfa z-score at 1.0', 'WHO wfl z-score at age 1.0', 'WHO lfa z-score at age 1.0', 'HC at 0.8',
                     'HC at 1.0', 'WHO wfa z-score at 1.0', 'WHO wfl z-score at age 1.0', 'WHO lfa z-score at age 1.0'],
                    ['max of weightToAgeLevel1', 'max of weightDivAgeLevel1', 'min of weightToAgeLevel1',
                     'min of weightDivAgeLevel1', 'avg of weightToAgeLevel1', 'avg of weightDivAgeLevel1',
                     'max of weightToAgeLevel2', 'max of weightDivAgeLevel2', 'min of weightToAgeLevel2',
                     'min of weightDivAgeLevel2', 'avg of weightToAgeLevel2', 'avg of weightDivAgeLevel2',
                     'max of heightToAgeLevel1', 'max of heightDivAgeLevel1', 'min of heightToAgeLevel1',
                     'min of heightDivAgeLevel1', 'avg of heightToAgeLevel1', 'avg of heightDivAgeLevel1',
                     'max of heightToAgeLevel2', 'max of heightDivAgeLevel2', 'min of heightToAgeLevel2',
                     'min of heightDivAgeLevel2', 'avg of heightToAgeLevel2', 'avg of heightDivAgeLevel2',
                     'max of BMIToAgeLevel1', 'max of BMIDivAgeLevel1', 'min of BMIToAgeLevel1','min of BMIDivAgeLevel1',
                     'avg of BMIToAgeLevel1', 'avg of BMIDivAgeLevel1', 'max of BMIToAgeLevel2','max of BMIDivAgeLevel2',
                     'min of BMIToAgeLevel2', 'min of BMIDivAgeLevel2', 'avg of BMIToAgeLevel2',
                     'avg of BMIDivAgeLevel2']]
    elif nationality == Nationality.SWE:
        X, f = removeSwedishBadFeatures(X, f)
        features = [['sex', 'birthWeight (KG)', 'gestationalAge (Weeks)', 'birthMonth', 'season', 'preterm flag',
                     'Height at 0.0', 'Weight at 0.0', 'BMI at 0.0', 'fatherHeight (M)', 'motherHeight (M)', 'nation'],
                    ['Height at 0.1', 'Weight at 0.1', 'BMI at 0.1', 'WHO wfa z-score at 0.1',
                     'WHO wfl z-score at age 0.1', 'WHO lfa z-score at age 0.1', 'WHO wfa z-score at 0.1',
                     'WHO wfl z-score at age 0.1', 'WHO lfa z-score at age 0.1'], ['Height at 0.2', 'Weight at 0.2',
                     'BMI at 0.2', 'WHO wfa z-score at 0.2', 'WHO wfl z-score at age 0.2', 'WHO lfa z-score at age 0.2',
                     'WHO wfa z-score at 0.2', 'WHO wfl z-score at age 0.2', 'WHO lfa z-score at age 0.2'], [
                     'Height at 0.3', 'Weight at 0.3', 'BMI at 0.3', 'WHO wfa z-score at 0.3',
                     'WHO wfl z-score at age 0.3', 'WHO lfa z-score at age 0.3', 'WHO wfa z-score at 0.3',
                     'WHO wfl z-score at age 0.3', 'WHO lfa z-score at age 0.3'], ['Height at 0.4', 'Weight at 0.4',
                     'BMI at 0.4', 'WHO wfa z-score at 0.4', 'WHO wfl z-score at age 0.4', 'WHO lfa z-score at age 0.4',
                     'WHO wfa z-score at 0.4', 'WHO wfl z-score at age 0.4', 'WHO lfa z-score at age 0.4'],
                    ['Height at 6 months (m)', 'Weight at 6 months (KG)', "Height at 6 months (m) Avg'd",
                     "Weight at 6 months (KG) Avg'd", 'Height at 0.5', 'Weight at 0.5', 'BMI at 0.5',
                     'WHO wfa z-score at 0.5', 'WHO wfl z-score at age 0.5', 'WHO lfa z-score at age 0.5',
                     'WHO wfa z-score at 0.5', 'WHO wfl z-score at age 0.5', 'WHO lfa z-score at age 0.5'],
                    ['Height at 0.6', 'Weight at 0.6', 'BMI at 0.6', 'WHO wfa z-score at 0.6',
                     'WHO wfl z-score at age 0.6', 'WHO lfa z-score at age 0.6', 'WHO wfa z-score at 0.6',
                     'WHO wfl z-score at age 0.6', 'WHO lfa z-score at age 0.6'], ['Height at 0.8', 'Weight at 0.8',
                     'BMI at 0.8', 'WHO wfa z-score at 0.8', 'WHO wfl z-score at age 0.8', 'WHO lfa z-score at age 0.8',
                     'WHO wfa z-score at 0.8', 'WHO wfl z-score at age 0.8', 'WHO lfa z-score at age 0.8'],
                    ['max of weightToAgeLevel1', 'max of weightDivAgeLevel1', 'min of weightToAgeLevel1',
                     'min of weightDivAgeLevel1', 'avg of weightToAgeLevel1', 'avg of weightDivAgeLevel1',
                     'max of weightToAgeLevel2', 'max of weightDivAgeLevel2', 'min of weightToAgeLevel2',
                     'min of weightDivAgeLevel2', 'avg of weightToAgeLevel2', 'avg of weightDivAgeLevel2',
                     'max of heightToAgeLevel1', 'max of heightDivAgeLevel1', 'min of heightToAgeLevel1',
                     'min of heightDivAgeLevel1', 'avg of heightToAgeLevel1', 'avg of heightDivAgeLevel1',
                     'max of heightToAgeLevel2', 'max of heightDivAgeLevel2', 'min of heightToAgeLevel2',
                     'min of heightDivAgeLevel2', 'avg of heightToAgeLevel2', 'avg of heightDivAgeLevel2',
                     'max of BMIToAgeLevel1', 'max of BMIDivAgeLevel1', 'min of BMIToAgeLevel1',
                     'min of BMIDivAgeLevel1', 'avg of BMIToAgeLevel1', 'avg of BMIDivAgeLevel1',
                     'max of BMIToAgeLevel2', 'max of BMIDivAgeLevel2', 'min of BMIToAgeLevel2',
                     'min of BMIDivAgeLevel2', 'avg of BMIToAgeLevel2', 'avg of BMIDivAgeLevel2']]
    for f_list in features:
        new_X = []
        for index in range(0, len(X)):
            new_X.append([])
        for feature in f_list:
            i = f.index(feature)
            for index in range(0, len(X)):
                new_X[index].append(X[index][i])
        features_groups.append(new_X)
    return features_groups


def findEarlyFeatureGroup(features_groups, c, final_classifier, scoring_class, k):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    index = 0
    for X in features_groups:
        if k < len(X[0]):
            new_X = RFE(scoring_class, k=k, step=1).fit_transform(X, c)
        final_classifier.fit(new_X, c)
        score = abs(np.mean(cross_val_score(final_classifier, new_X, c, cv=crossvalidation,
                                            scoring='neg_mean_squared_error')))
        print("Group number: ", index, "MSE:", score)
        index += 1


# Perform the fourth stage experiment
def program(vectors, final_classifiers, classFeatureSelectionData, regFeatureSelectionData):
    is_classi, is_regrassor, sw_classi, sw_regrassor = final_classifiers
    is_X, is_c, is_f, sw_X, sw_c, sw_f = vectors
    ISclassScoring, ISclassK, SWclassScoring, SWclassk = classFeatureSelectionData
    ISregScoring, ISregK, SWregScoring, SWregk = regFeatureSelectionData
    is_features_groups = divideToFeaturesGroups(Nationality.ISR, is_X, is_f)
    sw_features_groups = divideToFeaturesGroups(Nationality.SWE, sw_X, sw_f)
    # print("Israeli classifier: ")
    # findEarlyFeatureGroup(is_features_groups, is_c, is_classi, ISclassScoring, ISclassK)
    # print("Israeli regressor: ")
    # findEarlyFeatureGroup(is_features_groups, is_c, is_regrassor, ISregScoring, ISregK)
    print("Swedish classifier: ")
    findEarlyFeatureGroup(sw_features_groups, sw_c, sw_classi, SWclassScoring, SWclassk)
    # print("Swedish regressor: ")
    # findEarlyFeatureGroup(sw_features_groups, sw_c, sw_regrassor, SWregScoring, SWregk)


def experimentProgram(israeliChildrenList, swedishChildrenList):
    is_f, is_X, is_c = getDataForClassification(israeliChildrenList)
    sw_f, sw_X, sw_c = getDataForClassification(swedishChildrenList)
    vectors = is_X, is_c, is_f, sw_X,  sw_c, sw_f

    with open(finalclassifierpath(PICKLE_RECOMMENDED_FILE), "rb") as pklfile:
        rec_classifier = pkl.load(pklfile)

    is_classi = rec_classifier.getIsClassi()
    is_regrassor = rec_classifier.getIsRegrassor()
    sw_classi = rec_classifier.getSwClassi()
    sw_regrassor = rec_classifier.getSwRegrassor()
    final_classifiers = is_classi, is_regrassor, sw_classi, sw_regrassor
    is_r_forest = RandomForestClassifier(max_depth=10, max_features=0.3, random_state=1, min_samples_split=2,
                                         min_samples_leaf=2, n_estimators=35)
    is_AB = AdaBoostClassifier(base_estimator=is_r_forest, n_estimators=113, random_state=1)
    sw_r_forest = RandomForestClassifier(max_depth=10, max_features=0.7, random_state=1, min_samples_split=2,
                                         min_samples_leaf=2, n_estimators=12)
    sw_AB = AdaBoostClassifier(base_estimator=sw_r_forest, n_estimators=72, random_state=1)
    classFeatureSelectionData = is_AB, 22, sw_AB, 12
    is_r_forest = RandomForestClassifier(max_depth=10, max_features=0.75, random_state=1, min_samples_split=2,
                                         min_samples_leaf=10, n_estimators=12)
    is_AB = AdaBoostClassifier(base_estimator=is_r_forest, n_estimators=141, random_state=1)
    sw_r_forest = RandomForestClassifier(max_depth=30, max_features=0.85, random_state=1, min_samples_split=2,
                                         min_samples_leaf=16, n_estimators=45)
    regFeatureSelectionData = is_AB, 24, sw_r_forest, 13
    program(vectors, final_classifiers, classFeatureSelectionData, regFeatureSelectionData)



