from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from sklearn import tree
import numpy as np


# Print information about all the parameters in order to determine the wanted ranges
def determineRanges(X, c):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    imputer = Imputer(strategy='mean', axis=0)
    X = imputer.fit_transform(X)  # instead of fit

    # Number of trees in the forrest
    for N in range(1, 201):
        regression_tree = tree.DecisionTreeRegressor(n_estimators=N)
        regression_tree.fit(X, c)
        score = np.mean(
            cross_val_score(regression_tree, X, c, scoring='neg_mean_squared_error', cv=crossvalidation, n_jobs=1))
        print("Number of trees: %i MSE: %.3f" % (N, abs(score)))

    # Percentage of features that are considered at each split
    for P in np.arange(0.1, 1.05, 0.5):
        regression_tree = tree.DecisionTreeRegressor(max_features=P)
        regression_tree.fit(X, c)
        score = np.mean(
            cross_val_score(regression_tree, X, c, scoring='neg_mean_squared_error', cv=crossvalidation, n_jobs=1))
        print("Percentage of features: %i MSE: %.3f" % (P, abs(score)))

    # Max depth
    for D in range(1, 90):
        regression_tree = tree.DecisionTreeRegressor(max_depth=D)
        regression_tree.fit(X, c)
        score = np.mean(
            cross_val_score(regression_tree, X, c, scoring='neg_mean_squared_error', cv=crossvalidation, n_jobs=1))
        print("Max depth: %i MSE: %.3f" % (D, abs(score)))

    # Min samples in leaf
    for L in range(5, 100, 5):
        regression_tree = tree.DecisionTreeRegressor(min_samples_leaf=L)
        regression_tree.fit(X, c)
        score = np.mean(
            cross_val_score(regression_tree, X, c, scoring='neg_mean_squared_error', cv=crossvalidation, n_jobs=1))
        print("Min samples in leaf: %i MSE: %.3f" % (L, abs(score)))

    # Min samples to split
    for S in range(10, 200, 10):
        regression_tree = tree.DecisionTreeRegressor(min_samples_split=S)
        regression_tree.fit(X, c)
        score = np.mean(
            cross_val_score(regression_tree, X, c, scoring='neg_mean_squared_error', cv=crossvalidation, n_jobs=1))
        print("Min samples to split: %i MSE: %.3f" % (S, abs(score)))


def parametersTuning():
    pass

