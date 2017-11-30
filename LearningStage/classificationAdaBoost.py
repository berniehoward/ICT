from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from simpleai.search.local import hill_climbing
from LearningStage.parametersTuningLocalSearch import ParametersTuningLocalSearch
from Parser.auxiliary import Nationality, NA
from LearningStage.utility import removeNationFeature
from LearningStage.featureSelection import *
import numpy as np


# Create boolean "AdaBoost" by given arguments
def booleanAdaBoostCreator(f, X, c, args):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    imputer = Imputer(strategy='median', axis=0)
    X = imputer.fit_transform(X)

    if len(args) == 6:
        N_ES, N, P, D, L, S = args
    else:
        N_ES, N, P, D, L = args
        S = 2  # default value

    r_forest = RandomForestClassifier(max_depth=D, max_features=P, random_state=1, min_samples_split=S,
                                      min_samples_leaf=L, n_estimators=N)
    classifier = AdaBoostClassifier(base_estimator=r_forest, n_estimators=N_ES, random_state=1)
    classifier.fit(X, c)
    score = np.mean(
        cross_val_score(classifier, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return classifier, (1 - abs(score))


# Print information about all the parameters in order to determine the wanted ranges
def determineRanges(f, X, c, function):

    # Parameters: n_est, n trees , max_features, max_depth, min_samples_leaf, min_samples_split
    ranges = [range(1, 151), range(1, 201), np.arange(0.1, 1.05, 0.05), range(1, 90), range(5, 100, 5),
              range(10, 200, 10)]
    default_parameters = [50, 10, "auto", None, 1, 2]
    headers = ["Number of estimators", "Number of trees:", "Percentage of features:", "Max depth:",
               "Min samples in leaf:", "Min samples to split:"]

    for r in range(0, len(ranges)):
        for i in ranges[r]:
            args = default_parameters
            args[r] = i
            classifier, score = function(f, X, c, args)
            print(headers[r], " %.2f, MSE: %.3f" % (i, abs(score)))


# Perform the experiment for boolean AdaBoost:
def booleanAdaExp(f, X, c, experiment):
    print("%s ranges: " % experiment)
    determineRanges(f, X, c, booleanAdaBoostCreator)


def booleanAdaTuning(f, X, c, function ,ranges):
    boolClass = False  # Boolean classification
    AB_hops = [1, 1, 0.05, 1, 5]
    problem = ParametersTuningLocalSearch(ranges, f, X, c, AB_hops, function, "AB", boolClass)
    return hill_climbing(problem, 1000).state


def createFinalAdaboostClassifier(X, c, f, k, forest, printMode=False):
    selector = RFE(forest, k, step=1)
    new_X = selector.fit_transform(X, c)
    selector = selector.fit(X, c)
    new_f = []
    i = 0
    for b in selector.get_support():
        if b:
            new_f.append(f[i])
        i += 1

    if printMode:
        print(k, " best features are: ", new_f)

    forest.fit(new_X, c)
    return new_f, forest


def booleanAdaFeatureSelectionAndFinalClassifier(is_X, is_f, is_c, sw_X, sw_f, sw_c):
    isr_forest = RandomForestClassifier(max_depth=2, max_features=0.3, random_state=1,
                                      min_samples_leaf=10, n_estimators=35)
    isr_classifier = AdaBoostClassifier(base_estimator=isr_forest, n_estimators=113, random_state=1)

    swe_forest = RandomForestClassifier(max_depth=2, max_features=0.7, random_state=1,
                                   min_samples_leaf=20, n_estimators=12)
    swe_classifier = AdaBoostClassifier(base_estimator=swe_forest, n_estimators=72, random_state=1)


    # altrenative as expalined the summary work
    # isr_forest_alt = RandomForestClassifier(max_depth=2, random_state=1)
    # isr_classifier_alt = AdaBoostClassifier(base_estimator=isr_forest_alt, random_state=1)

    # swe_forest_alt = RandomForestClassifier(max_depth=None, max_features=0.7, random_state=1,
    #                                min_samples_leaf=1, n_estimators=10)
    # swe_classifier_alt = AdaBoostClassifier(base_estimator=swe_forest_alt, n_estimators=50, random_state=1)


    # Feature selection:
    print("Feature selection: ")
    imputer = Imputer(strategy='median', axis=0)
#
    is_X, f = removeNationFeature(is_X, is_f)
    is_X = imputer.fit_transform(is_X)
    # performSelectKBestFeatures(is_X, is_c, isr_classifier, Nationality.ISR.name)
#
    sw_X, f = removeNationFeature(sw_X, sw_f)
    sw_X = imputer.fit_transform(sw_X)
    # performSelectKBestFeatures(sw_X, sw_c, swe_classifier, Nationality.SWE.name)

    # performRFE(is_X, is_c, isr_classifier, Nationality.ISR.name)
    # performRFE(sw_X, sw_c, swe_classifier, Nationality.SWE.name)

    # performRFE(is_X, is_c, isr_classifier_alt, Nationality.ISR.name)
    # performRFE(sw_X, sw_c, swe_classifier_alt, Nationality.SWE.name)
#
    # # create final classification forest :
    is_k = 22
    sw_k = 12
#
    # isr_f, isr_final_RF = createFinalAdaboostClassifier(is_X, is_c, is_f, is_k, isr_classifier, True)
    swe_f, swe_final_RF = createFinalAdaboostClassifier(sw_X, sw_c, sw_f, sw_k, swe_classifier, True)
    # return isr_f, isr_final_RF, swe_f, swe_final_RF



