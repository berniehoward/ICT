from sklearn.feature_selection import SelectKBest, f_regression, f_classif, RFE
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import warnings
from sklearn.svm import SVR, SVC


# Perform feature selection and remain with k best features
# Return the best k features, the best k and the best mse
def selectKBestFeatures(X, c, forest, classifier_type, scoringFunction=f_regression):
    warnings.filterwarnings("ignore", category=UserWarning)
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    imputer = Imputer(strategy='median', axis=0)
    X = imputer.fit_transform(X)
    print("Range of K : [10, %i]" % len(X[0]))
    scores = []
    min_score = 1000
    for k in range(10, len(X[0])):
        new_X = SelectKBest(scoringFunction, k=k).fit_transform(X, c)
        forest.fit(new_X, c)
        score = abs(np.mean(cross_val_score(forest, new_X, c, cv=crossvalidation, scoring='neg_mean_squared_error')))
        scores.append(score)
        if score < min_score:
            min_score = score
            best_X = new_X
            best_k = k
    print(classifier_type, " mse: ")
    print(scores)
    return best_X, best_k, min_score


# Perform feature selection by "select k best features" strategy
def performSelectKBestFeatures(X, c, forest, origin):
    print("selectKBestFeatures: ")
    print("%s: " % origin)
    if set(c) == {0, 1}:  # Check if boolean classification or regression
        best_X, best_k, min_score = selectKBestFeatures(X, c, forest, "f_classif: ", f_classif)
    else:
        best_X, best_k, min_score = selectKBestFeatures(X, c, forest, "f_regression: ")
    print("K: ", best_k, "MSE/ACC: ", min_score)

    # nested function designed to be passed to selectKBestFeatures
    def scoringFunction(X, c):
        forest.fit(X, c)
        return forest.feature_importances_

    best_X, best_k, min_score = selectKBestFeatures(X, c, forest, "scoring function: ", scoringFunction)
    print("K: ", best_k, "MSE/ACC: ", min_score)


# Perform recursive feature selection and remain with k best features
# Return the best k and the best mse after the feature selection
def rfe(X, c, estimator, forest):
    scores = []
    min_score = 1000
    for k in range(10, len(X[0])):
        print(k)
        crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
        new_X = RFE(estimator, k, step=1).fit_transform(X, c)
        forest.fit(new_X, c)
        score = abs(np.mean(cross_val_score(forest, new_X, c, cv=crossvalidation, scoring='neg_mean_squared_error')))
        scores.append(score)
        if score < min_score:
            min_score = score
            best_k = k
    print(scores)
    return best_k, min_score


# Perform feature selection by "RFE" strategy
def performRFE(X, c, forest, origin):
    print("RFE: ")

    print("%s: " % origin)
    best_k, min_score = rfe(X, c, forest, forest)
    print("RF - k: ", best_k, "mse: ", min_score)
    if set(c) == {0, 1}:  # SVM
        print("SVC: ")
        estimator = SVC(kernel="linear")
        best_k, min_score = rfe(X, c, estimator, forest)
        print("SVC - k: ", best_k, "mse: ", min_score)
    else:
        print("SVR: ")  # SVR
        estimator = SVR(kernel="linear")
        best_k, min_score = rfe(X, c, estimator, forest)
        print("SVR - k: ", best_k, "mse: ", min_score)


