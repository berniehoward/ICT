from sklearn.feature_selection import SelectKBest, f_regression, RFE
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import Imputer
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import warnings
from sklearn.svm import SVR


# Perform feature selection and remain with k best features
# Return the best k features, the best k and the best mse
def selectKBestFeatures(X, c, forest, string, scoringFunction=f_regression):
    warnings.filterwarnings("ignore", category=RuntimeWarning)
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    imputer = Imputer(strategy='median', axis=0)
    X = imputer.fit_transform(X)
    print("range of k : [10, ", len(X[0]), "]")
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
    print(string, " mse: ")
    print(scores)
    return best_X, best_k, min_score


# Perform feature selection by "select k best features" strategy
def performSelectKBestFeatures(is_X, is_c, is_forest, sw_X, sw_c, sw_forest):
    print("selectKBestFeatures: ")

    print("Israeli: ")
    best_X, best_k, min_score = selectKBestFeatures(is_X, is_c, is_forest, "f_regression: ")
    print("k: ", best_k, "mse: ", min_score)
    best_X, best_k, min_score = selectKBestFeatures(is_X, is_c, is_forest, "scoring function: ",
                                                    scoringIsraeliRegressorFunction)
    print("k: ", best_k, "mse: ", min_score)

    print("Swedish: ")
    best_X, best_k, min_score = selectKBestFeatures(sw_X, sw_c, sw_forest, "f_regression: ")
    print("k: ", best_k, "mse: ", min_score)
    best_X, best_k, min_score = selectKBestFeatures(sw_X, sw_c, sw_forest, "scoring function: ",
                                                    scoringSwedishRegressorFunction)
    print("k: ", best_k, "mse: ", min_score)


#################################### scoring function for different database ####################################
def scoringIsraeliRegressorFunction(X, c):
    r_forest = RandomForestRegressor(max_depth=20, max_features=0.8, random_state=1, min_samples_split=2,
                                     min_samples_leaf=10, n_estimators=143)
    r_forest.fit(X, c)
    return r_forest.feature_importances_


def scoringSwedishRegressorFunction(X, c):
    r_forest = RandomForestRegressor(max_depth=16, max_features=0.85, random_state=1, min_samples_split=2,
                                     min_samples_leaf=30, n_estimators=45)
    r_forest.fit(X, c)
    return r_forest.feature_importances_

#######################################################################################################################


# Perform recursive feature selection and remain with k best features
# Return the best k and the best mse after the feature selection
def ref(X, c, estimator, forest):
    scores = []
    min_score = 1000
    for k in range(10, len(X[0])):
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


# Perform feature selection by "REF" strategy
def performREF(is_X, is_c, is_forest, sw_X, sw_c, sw_forest):
    print("REF: ")
    estimator = SVR(kernel="linear")

    print("Israeli: ")
    best_k, min_score = ref(is_X, is_c, is_forest, is_forest)
    print("RF - k: ", best_k, "mse: ", min_score)
    best_k, min_score = ref(is_X, is_c, estimator, is_forest)
    print("SVR - k: ", best_k, "mse: ", min_score)

    print("Swedish: ")
    best_k, min_score = ref(sw_X, sw_c, sw_forest, sw_forest)
    print("k: ", best_k, "mse: ", min_score)
    best_k, min_score = ref(sw_X, sw_c, estimator, sw_forest)
    print("k: ", best_k, "mse: ", min_score)


