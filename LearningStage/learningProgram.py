from Parser.auxiliary import NA
from LearningStage.utility import getTenMostCommonAges
from LearningStage.expProg import getDataForClassification
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from sklearn.svm import SVR, NuSVR
from sklearn.tree import export_graphviz
from pydotplus import graph_from_dot_data
from sklearn import tree
import six, os, time, itertools
import numpy as np
from math import ceil

def getDataForClassification(children):
    data = []
    classifications = []
    features = []
    checkFlag = False
    common_ages = sorted(getTenMostCommonAges(children, 8))
    for ch in children:
        if len(ch.goodSamples) == 0:
            continue
        f, d, c = ch.generateParametersForRegressionDecisionTree(common_ages, False)
        if not checkFlag:
            features = [i for i in f]
        if not c:
            continue
        data.append([x if x != NA else np.NaN for x in d])
        classifications.append(c)
        checkFlag = True
    return features, data, classifications

def regressionTreeCreator(f, X, c):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    for depth in range(1, 10):
        imputer = Imputer(strategy='mean', axis=0)
        X = imputer.fit_transform(X)  # instead of fit
        regression_tree = tree.DecisionTreeRegressor(random_state=0, min_samples_split=30,
                                                     min_samples_leaf=10)
        regression_tree.fit(X, c)
        if depth == 9:
            dotfile = six.StringIO()
            tree.export_graphviz(regression_tree, feature_names=f, out_file=dotfile)
            graph_from_dot_data(dotfile.getvalue()).write_png('tree' + str(depth) + '.png')
        if regression_tree.fit(X, c).tree_.max_depth < depth:
            break
        score = np.mean(
            cross_val_score(regression_tree, X, c, scoring='neg_mean_squared_error', cv=crossvalidation, n_jobs=1))
        print("Depth: %i MSE: %.3f" % (depth, abs(score)))

def exportTreesFromRegressionForest(f, r_forest):
    rf_path = os.path.join(os.getcwd(), "RegressionForest")
    os.system("del /f /q "+rf_path+"\\*")
    os.chdir(rf_path)
    for regression_tree in r_forest.estimators_:
            dotfile = six.StringIO()
            tree.export_graphviz(regression_tree, feature_names=f, out_file=dotfile)
            graph_from_dot_data(dotfile.getvalue()).write_png('tree_' + str(r_forest.estimators_.index(regression_tree))
            +'.png')

def printVectors(f, X):
    for x in X:
        print("feature number:", len(x),[(fe,x) for fe, x in zip(f,x)])

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

# Random Forest Regressor function example
def regressionForestCreatorAux(f, X, c, args):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    imputer = Imputer(strategy='median', axis=0)
    fn, msl, m, d, s = args
    X = imputer.fit_transform(X)  # instead of fit
    r_forest = RandomForestRegressor(max_depth=d, max_features=m, random_state=1,
                                     min_samples_split = s, min_samples_leaf = msl,
                                     n_estimators=fn)
    r_forest.fit(X, c)
    score = np.mean(
        cross_val_score(r_forest, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return r_forest, score

# wrapper function for learning subfunctions
def regressionForestCreator(f, X, c, function, usePerm = False):
    bestForest, best_m, best_msl, bestMSE = None, 0, 0, 1.0
    s = [range(1, 21), range(10, 110, 10),
         [x/100 for x in range(30,100,5)], range(3, 31), range(2, 41)]
    if usePerm:
        permutations = list(itertools.product(*s)) #all permutations
        for fn,msl,m,d,s in permutations:
            args = [fn, msl, m, d, s]
            r_forest, score = function(f, X, c, args)
            if abs(score) < bestMSE:
                bestForest, best_m, best_msl, bestMSE = r_forest, m, msl, abs(score)
    else:
        # fn, msl, m, d, s
        args = [10, 1, 1.0, 100, 2] #n_est, min_samples_leaf, features, depth, n_split
        for arg in s:
            for i in arg:
                args[s.index(arg)] = i
                r_forest, score = function(f, X, c, args)
                if abs(score) < bestMSE:
                    bestForest, best_m, best_msl, bestMSE = r_forest, args[2], args[1], abs(score)
            args = [10, 1, "auto", None, 2]
            print("Min Samples In Leaf: %i, max_features: %.2f precent, MSE: %.3f" % (best_msl, best_m, abs(bestMSE)))
            bestForest, best_m, best_msl, bestMSE = None, 0, 0, 1.0
    #exportTreesFromRegressionForest(f, bestForest)
    return r_forest

def createRandomForestRegressorAndClassifyData(swedishChildrenList, israeliChildrenList, printFlag = True):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/' #for plotting trees
    f, X, c = getDataForClassification(israeliChildrenList)
    #printVectors(f,X)
    # regressionTreeCreator(f, X, c)
    forest = regressionForestCreator(f, X, c, regressionForestCreatorAux, False)
    #classifyData(forest, children)




