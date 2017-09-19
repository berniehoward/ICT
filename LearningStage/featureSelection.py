from sklearn.feature_selection import mutual_info_regression
from sklearn.feature_selection import SelectKBest, SelectPercentile
from sklearn.feature_selection import f_regression
from sklearn.feature_selection import RFE
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import Imputer
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import warnings


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


def univariateFeatureSelection(f, X, c, p):
    X_new = SelectPercentile(f_regression, percentile=p).fit_transform(X, c)
    return X_new


def getForestFeatues(f, r_forest):
    importances = r_forest.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("Feature ranking:")
    # for i in range(len(f)):
    #     print("feature %d (%f)" % (indices[i], f[i]))
    return indices
