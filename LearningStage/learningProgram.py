from sklearn.model_selection import cross_val_score
from sklearn.ensemble import AdaBoostRegressor
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from sklearn.svm import SVR, NuSVR
from sklearn.tree import export_graphviz
from pydotplus import graph_from_dot_data
from sklearn import tree
import six, os, time, itertools
import numpy as np


# TODO - is this relevant or we should delete it?
# def regressionTreeCreator(f, X, c):
#     crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
#     for depth in range(1, 10):
#         imputer = Imputer(strategy='mean', axis=0)
#         X = imputer.fit_transform(X)  # instead of fit
#         regression_tree = tree.DecisionTreeRegressor(random_state=0, min_samples_split=30,
#                                                      min_samples_leaf=10)
#         regression_tree.fit(X, c)
#         if depth == 9:
#             dotfile = six.StringIO()
#             tree.export_graphviz(regression_tree, feature_names=f, out_file=dotfile)
#             graph_from_dot_data(dotfile.getvalue()).write_png('tree' + str(depth) + '.png')
#         if regression_tree.fit(X, c).tree_.max_depth < depth:
#             break
#         score = np.mean(
#             cross_val_score(regression_tree, X, c, scoring='neg_mean_squared_error', cv=crossvalidation, n_jobs=1))
#         print("Depth: %i MSE: %.3f" % (depth, abs(score)))


def exportTreesFromRegressionForest(f, r_forest):
    rf_path = os.path.join(os.getcwd(), "RegressionForest")
    os.system("del /f /q "+rf_path+"\\*")
    os.chdir(rf_path)
    for regression_tree in r_forest.estimators_:
            dotfile = six.StringIO()
            tree.export_graphviz(regression_tree, feature_names=f, out_file=dotfile)
            graph_from_dot_data(dotfile.getvalue()).write_png('tree_' + str(r_forest.estimators_.index(regression_tree))
            +'.png')

# AdaBoost function example
def adaBoostCreatorAux(f, X, c, msl, m):
    crossvalidation = KFold(n_splits=4, shuffle=True, random_state=1)
    imputer = Imputer(strategy='mean', axis=0)
    X = imputer.fit_transform(X)  # instead of fit
    r_forest = AdaBoostRegressor(n_estimators=50, random_state=1)
    r_forest.fit(X, c)
    score = np.mean(
        cross_val_score(r_forest, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return r_forest, score


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






