from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
import numpy as np


# Create boolean "AdaBoost" by given arguments
def AdaBoostCreator(f, X, c, args):
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
    return classifier, 1 - score


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
    determineRanges(f, X, c, AdaBoostCreator)


def booleanAdaTuning():
    # TODO - complete
    pass


def booleanAdaFeatureSelectionAndFinalClassifier():
    # TODO - complete
    pass

