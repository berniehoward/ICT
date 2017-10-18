from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from LearningStage.boolAdaBoost import determineRanges
import numpy as np


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


# Perform the experiment for boolean AdaBoost:
def regressionAdaExp(f, X, c, experiment):
    print("%s ranges: " % experiment)
    determineRanges(f, X, c, regressionAdaBoostCreator)


def regressionAdaTuning():
    # TODO - complete
    pass


def regressionAdaFeatureSelectionAndFinalClassifier():
    # TODO - complete
    pass

