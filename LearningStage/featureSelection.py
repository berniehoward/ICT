from sklearn.feature_selection import mutual_info_regression
from sklearn.feature_selection import SelectKBest, SelectPercentile
from sklearn.feature_selection import chi2, f_regression
from sklearn.feature_selection import RFE
import numpy as np

def selectKBestFeatures(X, c, K):
    X_new = SelectKBest(f_regression, k=K).fit_transform(X, c) # chi squared test
    return X_new

def univariateFeatureSelection(f, X, c, p):
    X_new = SelectPercentile(f_regression, percentile=p).fit_transform(X, c) # with Univariate linear regression tests.
    return X_new

def getForestFeatues(f, r_forest):
    importances = r_forest.feature_importances_
    indices = np.argsort(importances)[::-1]
    print("Feature ranking:")
    # for i in range(len(f)):
    #     print("feature %d (%f)" % (indices[i], f[i]))
    return indices