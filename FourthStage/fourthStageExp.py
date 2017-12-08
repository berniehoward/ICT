from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import Imputer
from LearningStage.classificationRandomForest import getDataForBooleanClassification
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
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
                     'nation'], ['Height at 0.1', 'Weight at 0.1', 'BMI at 0.1', 'WHO wfa z-score at 0.1',
                     'WHO wfl z-score at age 0.1', 'WHO lfa z-score at age 0.1', 'WHO hcfa z-score at 0.1', 'HC at 0.1'],
                    ['Height at 0.2', 'Weight at 0.2', 'BMI at 0.2', 'WHO wfa z-score at 0.2',
                     'WHO wfl z-score at age 0.2', 'WHO lfa z-score at age 0.2', 'WHO hcfa z-score at 0.2', 'HC at 0.2']
                    , ['Height at 0.3', 'Weight at 0.3', 'BMI at 0.3',
                     'WHO wfa z-score at 0.3', 'WHO wfl z-score at age 0.3', 'WHO lfa z-score at age 0.3',
                     'WHO hcfa z-score at 0.3', 'HC at 0.3'], ['Height at 0.4', 'Weight at 0.4',
                     'BMI at 0.4', 'WHO wfa z-score at 0.4', 'WHO wfl z-score at age 0.4', 'WHO lfa z-score at age 0.4',
                     'HC at 0.4', 'WHO hcfa z-score at 0.4'], ['Height at 6 months (m)', 'Weight at 6 months (KG)',
                     "Height at 6 months (m) Avg'd", "Weight at 6 months (KG) Avg'd", 'Weight at 0.5', 'BMI at 0.5',
                     'WHO wfa z-score at 0.5', 'WHO wfl z-score at age 0.5', 'WHO lfa z-score at age 0.5',
                     'WHO hcfa z-score at 0.5', 'HC at 0.5',  "HC at 6 months Avg'd", 'Avg brothers HC at 6 months (m)',
                     'Avg brothers Height at 6 months (m)', 'Avg brothers Weight at 6 months (m)', 'HC at 0.8']]
    elif nationality == Nationality.SWE:
        X, f = removeSwedishBadFeatures(X, f)
        features = [['sex', 'birthWeight (KG)', 'gestationalAge (Weeks)', 'birthMonth', 'season', 'preterm flag',
                     'Height at 0.0', 'Weight at 0.0', 'BMI at 0.0', 'fatherHeight (M)', 'motherHeight (M)', 'nation'],
                    ['Height at 0.1', 'Weight at 0.1', 'BMI at 0.1', 'WHO wfa z-score at 0.1',
                     'WHO wfl z-score at age 0.1', 'WHO lfa z-score at age 0.1'], ['Height at 0.2', 'Weight at 0.2',
                     'BMI at 0.2', 'WHO wfa z-score at 0.2', 'WHO wfl z-score at age 0.2',
                     'WHO lfa z-score at age 0.2'], ['Height at 0.3', 'Weight at 0.3', 'BMI at 0.3',
                     'WHO wfa z-score at 0.3', 'WHO wfl z-score at age 0.3', 'WHO lfa z-score at age 0.3'],
                    ['Height at 0.4', 'Weight at 0.4', 'BMI at 0.4', 'WHO wfa z-score at 0.4',
                     'WHO wfl z-score at age 0.4', 'WHO lfa z-score at age 0.4'], ['Height at 6 months (m)',
                     'Weight at 6 months (KG)', "Height at 6 months (m) Avg'd",
                     "Weight at 6 months (KG) Avg'd", 'Height at 0.5', 'Weight at 0.5', 'BMI at 0.5',
                     'WHO wfa z-score at 0.5', 'WHO wfl z-score at age 0.5', 'WHO lfa z-score at age 0.5'],
                    ['Height at 0.8', 'Weight at 0.8','BMI at 0.8', 'WHO wfa z-score at 0.8',
                     'WHO wfl z-score at age 0.8', 'WHO lfa z-score at age 0.8', 'WHO wfa z-score at 0.8']]
    unified_features = []
    for indx in range(0, len(features)):
        unified_features.append([])
        for j in range(0, indx + 1):
            unified_features[indx] += features[j]

    for f_list in unified_features:
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
    imputer = Imputer(strategy='median', axis=0)
    for X in features_groups:
        X  = imputer.fit_transform(X)
        if k < len(X[0]):
            new_X = RFE(scoring_class, k, step=1).fit_transform(X, c)
        else:
            new_X = RFE(scoring_class, len(X[0]), step=1).fit_transform(X, c)
        final_classifier.fit(new_X, c)
        score = abs(np.mean(cross_val_score(final_classifier, new_X, c, cv=crossvalidation,
                                            scoring='neg_mean_squared_error')))
        if set(c) == {0, 1}:
            score = 1 - score
        print("Group number: ", index, "ACC/MSE:", score)
        index += 1



# Perform the fourth stage experiment
def program(vectors, final_classifiers, classFeatureSelectionData, regFeatureSelectionData):
    is_classi, is_regrassor, sw_classi, sw_regrassor = final_classifiers
    class_is_f, class_is_X, class_is_c, class_sw_f, class_sw_X, class_sw_c, reg_is_f, reg_is_X, reg_is_c, \
    reg_sw_f, reg_sw_X, reg_sw_c = vectors
    ISclassScoring, ISclassK, SWclassScoring, SWclassk = classFeatureSelectionData
    ISregScoring, ISregK, SWregScoring, SWregk = regFeatureSelectionData
    class_is_features_groups = divideToFeaturesGroups(Nationality.ISR, class_is_X, class_is_f)
    reg_is_features_groups = divideToFeaturesGroups(Nationality.ISR, reg_is_X, reg_is_f)
    class_sw_features_groups = divideToFeaturesGroups(Nationality.SWE, class_sw_X, class_sw_f)
    reg_sw_features_groups = divideToFeaturesGroups(Nationality.SWE, reg_sw_X, reg_sw_f)
    print("Israeli classifier: ")
    findEarlyFeatureGroup(class_is_features_groups, class_is_c, is_classi, ISclassScoring, ISclassK)
    print("Israeli regressor: ")
    findEarlyFeatureGroup(reg_is_features_groups, reg_is_c, is_regrassor, ISregScoring, ISregK)
    print("Swedish classifier: ")
    findEarlyFeatureGroup(class_sw_features_groups, class_sw_c, sw_classi, SWclassScoring, SWclassk)
    print("Swedish regressor: ")
    findEarlyFeatureGroup(reg_sw_features_groups, reg_sw_c, sw_regrassor, SWregScoring, SWregk)


def experimentProgram(israeliChildrenList, swedishChildrenList):
    class_is_f, class_is_X, class_is_c = getDataForBooleanClassification(israeliChildrenList)
    class_sw_f, class_sw_X, class_sw_c = getDataForBooleanClassification(swedishChildrenList)
    reg_is_f, reg_is_X, reg_is_c = getDataForClassification(israeliChildrenList)
    reg_sw_f, reg_sw_X, reg_sw_c = getDataForClassification(swedishChildrenList)

    vectors = class_is_f, class_is_X, class_is_c, class_sw_f, class_sw_X, class_sw_c, reg_is_f, reg_is_X, reg_is_c, \
              reg_sw_f, reg_sw_X, reg_sw_c

    with open(finalclassifierpath(PICKLE_RECOMMENDED_FILE), "rb") as pklfile:
        rec_classifier = pkl.load(pklfile)

    is_classi = rec_classifier.getIsClassi()
    is_regrassor = rec_classifier.getIsRegrassor()
    sw_classi = rec_classifier.getSwClassi()
    sw_regrassor = rec_classifier.getSwRegrassor()
    final_classifiers = is_classi, is_regrassor, sw_classi, sw_regrassor

    # Classifiers :
    is_r_forest = RandomForestClassifier(max_depth=10, max_features=0.3, random_state=1, min_samples_split=2,
                                         min_samples_leaf=2, n_estimators=35)
    is_AB = AdaBoostClassifier(base_estimator=is_r_forest, n_estimators=113, random_state=1)
    sw_r_forest = RandomForestClassifier(max_depth=10, max_features=0.7, random_state=1, min_samples_split=2,
                                         min_samples_leaf=2, n_estimators=12)
    sw_AB = AdaBoostClassifier(base_estimator=sw_r_forest, n_estimators=72, random_state=1)
    classFeatureSelectionData = is_AB, 22, sw_AB, 12

    # Regressors:
    is_r_forest = RandomForestRegressor(max_depth=10, max_features=0.75, random_state=1, min_samples_split=2,
                                        min_samples_leaf=10, n_estimators=12)
    is_AB = AdaBoostRegressor(base_estimator=is_r_forest, n_estimators=141, random_state=1)
    sw_r_forest = RandomForestRegressor(max_depth=30, max_features=0.85, random_state=1, min_samples_split=2,
                                        min_samples_leaf=16, n_estimators=45)
    regFeatureSelectionData = is_AB, 24, sw_r_forest, 13

    program(vectors, final_classifiers, classFeatureSelectionData, regFeatureSelectionData)




