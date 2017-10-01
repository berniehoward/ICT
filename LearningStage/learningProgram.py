from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from sklearn.svm import SVR, NuSVR
import numpy as np


# SVR (Epsilon-Support Vector Regression) function example
def svrAux(f, X, c, msl, m):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    imputer = Imputer(strategy='mean', axis=0)
    X = imputer.fit_transform(X)  # instead of fit
    classifier = SVR(C=1.0, epsilon = 0.2)
    classifier.fit(X, c)
    score = np.mean(
        cross_val_score(classifier, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return classifier, score






