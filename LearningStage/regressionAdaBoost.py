from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from LearningStage.classificationAdaBoost import determineRanges
from LearningStage.regressionRandomForest import parametersTuning
import numpy as np
from LearningStage.featureSelection import *
from Parser.auxiliary import Nationality


# Create regression "AdaBoost" by given arguments
def regressionAdaBoostCreator(f, X, c, args):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    imputer = Imputer(strategy='median', axis=0)
    X = imputer.fit_transform(X)

    if len(args) == 6:
        N_ES, N, P, D, L, S = args
    else:
        N_ES, N, P, D, L = args
        S = 2  # default value

    r_forest = RandomForestRegressor(max_depth=D, max_features=P, random_state=1, min_samples_split=S,
                                     min_samples_leaf=L, n_estimators=N)
    classifier = AdaBoostRegressor(base_estimator=r_forest, n_estimators=N_ES, random_state=1)
    classifier.fit(X, c)
    score = np.mean(
        cross_val_score(classifier, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return classifier, abs(score)


# Perform the experiment for regression AdaBoost:
def regressionAdaExp(f, X, c, experiment):
    print("%s ranges: " % experiment)
    determineRanges(f, X, c, regressionAdaBoostCreator)


# Aid function for local search
def regressionAdaLocalSearch(vectors, ranges):
    is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c = vectors
    isr_ranges, swe_ranges, mixed_ranges, hops = ranges
    is_params, is_score = parametersTuning(is_f, is_X, is_c, regressionAdaBoostCreator, isr_ranges, hops, "AB")
    print("Israeli: ", " params: ", is_params, " score: ", is_score)
    sw_params, sw_score = parametersTuning(sw_f, sw_X, sw_c, regressionAdaBoostCreator, swe_ranges, hops, "AB")
    print("Swedish: ", " params: ", sw_params, " score: ", sw_score)
    mix_params, mix_score = parametersTuning(mix_f, mix_X, mix_c, regressionAdaBoostCreator, mixed_ranges, hops, "AB")
    print("Mix: ", " params: ", mix_params, " score: ", mix_score)


# Perform local search for regression AB
def regressionAdaTuning(params, vectors):
    print("Regression AB local search: ")

    isr_ranges, swe_ranges, mixed_ranges, isr_m_ranges, swe_m_ranges, mixed_m_ranges, isr_f_ranges, swe_f_ranges, \
    mixed_f_ranges, hops = params
    is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, mix_m_f, \
    mix_m_X, mix_m_c, is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c = vectors

    print("Bout Genders: ")
    BG_ranges = isr_ranges, swe_ranges, mixed_ranges, hops
    BG_vectors = is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c
    regressionAdaLocalSearch(BG_vectors, BG_ranges)
    print("Males: ")
    M_ranges = isr_m_ranges, swe_m_ranges, mixed_m_ranges, hops
    M_vectors = is_m_f, is_m_X, is_m_c, sw_m_f, sw_m_X, sw_m_c, mix_m_f, mix_m_X, mix_m_c
    regressionAdaLocalSearch(M_vectors, M_ranges)
    print("Females: ")
    F_ranges = isr_f_ranges, swe_f_ranges, mixed_f_ranges, hops
    F_vectors = is_f_f, is_f_X, is_f_c, sw_f_f, sw_f_X, sw_f_c, mix_f_f, mix_f_X, mix_f_c
    regressionAdaLocalSearch(F_vectors, F_ranges)


def regressionAdaFinalClassifier(is_X, is_c, is_f, is_k, sw_X, sw_c, sw_f, sw_k, regressors):
    isr_AB, swe_AB = regressors
    is_f, is_final_AB = createFinalRegressionAda(is_X, is_c, is_f, is_k, isr_AB, Nationality.ISR, True)
    sw_f, sw_final_AB = createFinalRegressionAda(sw_X, sw_c, sw_f, sw_k, swe_AB, Nationality.SWE, True)
    return is_f, is_final_AB, sw_f, sw_final_AB


# Return the recommended regressor
def createFinalRegressionAda(X, c, f, k, ab, nationality, printMode=False):
        if nationality == Nationality.ISR:
            selector = RFE(ab, k, step=1)
        else:
            def scoringFunction(X, c):
                ab.fit(X, c)
                return ab.feature_importances_
            selector = SelectKBest(scoringFunction, k=k)

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

        ab.fit(new_X, c)
        return new_f, ab
