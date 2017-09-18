from sklearn.feature_selection import mutual_info_regression
from sklearn.feature_selection import SelectKBest, SelectPercentile
from sklearn.feature_selection import chi2, f_regression
from sklearn.feature_selection import RFE
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import Imputer
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score


def selectKBestFeatures(X, c, scoringFunction):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    print("range of k : [10, ", len(X), "]")
    scores = []
    for k in range(10, len(X)):
        new_foredt = SelectKBest(scoringFunction, k=k)
        new_foredt.fit(X, c)
        scores.append(np.mean(cross_val_score(new_foredt, X, c, cv=crossvalidation, scoring='neg_mean_squared_error')))
    print("scoringFunction mse: ")
    print(scores)
    scores = []
    for k in range(10, len(X)):
        new_foredt = SelectKBest(f_regression, k=k)
        new_foredt.fit(X, c)
        scores.append(np.mean(cross_val_score(new_foredt, X, c, cv=crossvalidation, scoring='neg_mean_squared_error')))
    print("f_regression mse: ")
    print(scores)


def scoringIsraeliRegressorFunction(X, c):
    imputer = Imputer(strategy='median', axis=0)
    X = imputer.fit_transform(X)
    r_forest = RandomForestRegressor(max_depth=20, max_features=0.8, random_state=1, min_samples_split=2,
                                     min_samples_leaf=10, n_estimators=143)
    r_forest.fit(X, c)
    return r_forest.feature_importances_


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