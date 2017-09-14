from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from simpleai.search.local import hill_climbing
from LearningStage.parametersTuningLocalSearch import ParametersTuningLocalSearch
from LearningStage.utility import printVectors

def determineRanges(f, X, c, function):

    # Parameters: n_est, max_features, max_depth, min_samples_leaf, min_samples_split
    ranges = [range(1, 201), np.arange(0.1, 1.05, 0.05), range(1, 90), range(5, 100, 5), range(10, 200, 10)]
    default_parameters = [10, "auto", None, 1, 2]
    headers = ["Number of trees:", "Percentage of features:", "Max depth:", "Min samples in leaf:", "Min samples to split:"]

    for r in range(0, len(ranges)):
        for i in ranges[r]:
            args = default_parameters
            args[r] = i
            r_forest, score = function(f, X, c, args)
            print(headers[r], " %.2f, MSE: %.3f" % (i, abs(score)))


# Create "Random Forest" Regressor by given arguments
def randomForestCreator(f, X, c, args):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    imputer = Imputer(strategy='median', axis=0)
    if len(args) == 5:
        N, P, D, L, S = args
    else:
        N, P, D, L = args
        S = 2  # default value
    X = imputer.fit_transform(X)  # instead of fit
    r_forest = RandomForestClassifier(max_depth=D, max_features=P, random_state=1, min_samples_split=S,
                                     min_samples_leaf=L, n_estimators=N)
    r_forest.fit(X, c)
    score = np.mean(
        cross_val_score(r_forest, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return r_forest, score

def booleanTreesExp(is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, flag):
    print("Israeli ranges: ")
    determineRanges(is_f, is_X, is_c, randomForestCreator)
    print("Swedish ranges: ")
    determineRanges(sw_f, sw_X, sw_c, randomForestCreator)
    print("Mix ranges: ")
    determineRanges(mix_f, mix_X, mix_c, randomForestCreator)