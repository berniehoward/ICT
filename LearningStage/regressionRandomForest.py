from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from simpleai.search.local import hill_climbing
from LearningStage.parametersTuningLocalSearch import ParametersTuningLocalSearch
from LearningStage.utility import getTenMostCommonAges, splitByGender
from Parser.auxiliary import NA
from sklearn.feature_selection import RFE


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
def parametersTuning(f, X, c, function, ranges, hops, flag):
    problem = ParametersTuningLocalSearch(ranges, f, X, c, hops, function, flag)
    return hill_climbing(problem, 1000).state


# Perform the experiment of determine ranges for regression RF
def regressionForestExp(f, X, c, experiment):
    print("%s ranges: " % experiment)
    determineRanges(f, X, c, regressionForestCreator)


# Aid function for local search
def regressionForestLocalSearch(vectors, ranges):
    is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c = vectors
    isr_ranges, swe_ranges, mixed_ranges, hops = ranges
    is_params, is_score = parametersTuning(is_f, is_X, is_c, regressionForestCreator, isr_ranges, hops, "RF")
    print("Israeli: ", " params: ", is_params, " score: ", is_score * (-1))
    sw_params, sw_score = parametersTuning(sw_f, sw_X, sw_c, regressionForestCreator, swe_ranges, hops, "RF")
    print("Swedish: ", " params: ", sw_params, " score: ", sw_score * (-1))
    mix_params, mix_score = parametersTuning(mix_f, mix_X, mix_c, regressionForestCreator, mixed_ranges, hops, "RF")
    print("Mix: ", " params: ", mix_params, " score: ", mix_score * (-1))


# Perform local search for regression RF
def regressionForestTuning(params, vectors):
    print("Regression RF local search: ")

    isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, swe_f_ranges, \
    mixed_f_ranges, hops = params
    is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, mix_m_f, \
    mix_m_X, mix_m_c, is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c = vectors

    print("Bout Genders: ")
    BG_ranges = isr_ranges, swe_ranges, mixed_ranges, hops
    BG_vectors = is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c
    regressionForestLocalSearch(BG_vectors, BG_ranges)
    print("Males: ")
    M_ranges = isr_m_ranges, swe_m_ranges, mixed_m_ranges, hops
    M_vectors = is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, mix_m_f, mix_m_X, mix_m_c
    regressionForestLocalSearch(M_vectors, M_ranges)
    print("Females: ")
    F_ranges = isr_f_ranges, swe_f_ranges, mixed_f_ranges, hops
    F_vectors = is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c
    regressionForestLocalSearch(F_vectors, F_ranges)


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


# Return the recommended regression classifier
def createFinalRegressionForest(X, c, f, k, forest, printMode=False):
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


def regressionForestFeatureSelectionAndFinalClassifier():
    # TODO - complete
    pass

