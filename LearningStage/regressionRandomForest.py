from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from simpleai.search.local import hill_climbing
from LearningStage.parametersTuningLocalSearch import ParametersTuningLocalSearch


# Print information about all the parameters in order to determine the wanted ranges
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
def regressionForestCreator(f, X, c, args):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    imputer = Imputer(strategy='median', axis=0)
    if len(args) == 5:
        N, P, D, L, S = args
    else:
        N, P, D, L = args
        S = 2  # default value
    X = imputer.fit_transform(X)  # instead of fit
    r_forest = RandomForestRegressor(max_depth=D, max_features=P, random_state=1, min_samples_split=S,
                                     min_samples_leaf=L, n_estimators=N)
    r_forest.fit(X, c)
    score = np.mean(
    cross_val_score(r_forest, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return r_forest, score


# Perform parameters tuning in order to get the parameters which give as the best classifier
# Return bet_params, best_score
def parametersTuning(f, X, c, function, ranges, hops):
    problem = ParametersTuningLocalSearch(ranges, f, X, c, hops, function)
    return hill_climbing(problem, 1000).state


# Perform the experiment for regression trees:
def regressionTreesExp(is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, flag):
    # print("Israeli ranges: ")
    # determineRanges(is_f, is_X, is_c, regressionForestCreator)
    # print("Swedish ranges: ")
    # determineRanges(sw_f, sw_X, sw_c, regressionForestCreator)
    # print("Mix ranges: ")
    # determineRanges(mix_f, mix_X, mix_c, regressionForestCreator)

    if flag == 'mix':
        is_ranges = [range(128, 149), np.arange(0.1, 1.05, 0.05), range(20, 41), range(10, 30, 5)]
        sw_ranges = [range(39, 60), np.arange(0.25, 0.95, 0.05), range(3, 17), range(15, 35, 5)]
        mix_ranges = [range(56, 75), np.arange(0.25, 0.9, 0.05), range(3, 9), range(15, 45, 5)]
    if flag == 'M':
        is_ranges = [range(94, 114), range(0), range(12, 32), range(5, 20, 5)]
        sw_ranges = [range(48, 68),  range(0), range(5, 25), range(5, 30, 5)]
        mix_ranges = [range(83, 103),  range(0), range(5, 25), range(5, 35, 5)]
    if flag == 'F':
        is_ranges = [range(80, 95), np.arange(0.1, 0.5, 0.05),  range(0), range(5, 25, 5)]
        sw_ranges = [range(31, 51), np.arange(0.2, 1, 0.05), range(6, 26), range(5, 20, 5)]
        mix_ranges = [range(79, 99), np.arange(0.25, 1, 0.05), range(5, 25), range(5, 25, 5)]

    hops = [1, 0.05, 1, 5]
    is_params, is_score = parametersTuning(is_f, is_X, is_c, regressionForestCreator, is_ranges, hops)
    print("Israeli: ", " params: ", is_params, " score: ", is_score * (-1))
    sw_params, sw_score = parametersTuning(sw_f, sw_X, sw_c, regressionForestCreator, sw_ranges, hops)
    print("Swedish: ", " params: ", sw_params, " score: ", sw_score * (-1))
    mix_params, mix_score = parametersTuning(mix_f, mix_X, mix_c, regressionForestCreator, mix_ranges, hops)
    print("Mix: ", " params: ", mix_params, " score: ", mix_score * (-1))
