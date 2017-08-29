from Parser.auxiliary import NA
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from sklearn.tree import export_graphviz
from pydotplus import graph_from_dot_data
from sklearn import tree
import six, os, time, itertools
import numpy as np
from math import ceil
from joblib import Parallel

"""  
http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html#sklearn.ensemble.RandomForestRegressor
"""

def getDataForClassification(swedishChildrenList, israeliChildrenList):
    data = []
    classifications = []
    features = []
    checkFlag = False
    for ch in israeliChildrenList:
        if len(ch.goodSamples) == 0:
            continue
        f, d, c = ch.generateParametersForRegressionDecisionTree(False)
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
        regression_tree = tree.DecisionTreeRegressor(depth = None, random_state=0, min_samples_split=30,
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

# If depth == None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.
def regressionForestCreatorAux_FULL(f, X, c, k, fn, msl, m, d, s, f_time):
    print(k, fn, msl, m, d, s, float(format((time.time()-f_time)/60, '.2f')))
    crossvalidation = KFold(n_splits=k, shuffle=True, random_state=1)
    imputer = Imputer(strategy='mean', axis=0)
    X = imputer.fit_transform(X)  # instead of fit
    r_forest = RandomForestRegressor(max_depth=d, max_features=m, random_state=1,
                                     min_samples_split = s, min_samples_leaf = msl,
                                     n_estimators=fn)
    r_forest.fit(X, c)
    score = np.mean(
        cross_val_score(r_forest, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return r_forest, score

def regressionForestCreator_FULL(f, X, c):
    bestForest, best_m, best_msl, bestMSE = None, 0, 0, 1.0
    f_time = time.time()
    s = [range(2, 11), range(1, 21), range(10, 110, 10),
         [x/100 for x in range(30,100,5)], range(3, 31), range(2, 41)]
    permutations = list(itertools.product(*s)) #all permutations
    for k,fn,msl,m,d,s in permutations:
        r_forest, score = regressionForestCreatorAux_FULL(f, X, c, k, fn, msl, m, d, s, f_time)
        if abs(score) < bestMSE:
            bestForest, best_m, best_msl, bestMSE = r_forest, m, msl, abs(score)
    print("Min Samples In Leaf: %i, max_features: %.2f precent, MSE: %.3f" % (best_msl, best_m, abs(bestMSE)))
    exportTreesFromRegressionForest(f, bestForest)
    return r_forest

def classifyData(forest, children):
    for c in children:
        #TODO fv = getFeatureVector(c)
        predictation = forest.predict(fv)

def printVectors(f, X):
    for x in X:
        print("feature number:", len(x),[(fe,x) for fe, x in zip(f,x)])

def regressionForestCreatorAux(f, X, c, msl, m):
    crossvalidation = KFold(n_splits=2, shuffle=True, random_state=1)
    imputer = Imputer(strategy='mean', axis=0)
    X = imputer.fit_transform(X)  # instead of fit
    r_forest = AdaBoostRegressor(n_estimators=1000, random_state=1)
    r_forest.fit(X, c)
    score = np.mean(
        cross_val_score(r_forest, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return r_forest, score

def regressionForestCreator(f, X, c):
    bestForest, best_m, best_msl, bestMSE = None, 0, 0, 1.0
    f_time = time.time()
    for msl in range(10, 110, 10): # minimum samples in leaf
        for m in [x/100 for x in range(30,100,5)]: # percent of features
            r_forest, score = \
                        regressionForestCreatorAux(f, X, c, msl, m)
            if abs(score) < bestMSE:
                                bestForest, best_m, best_msl, bestMSE = r_forest, m, msl, abs(score)
    print("Min Samples In Leaf: %i, max_features: %.2f precent, MSE: %.3f" % (best_msl, best_m, abs(bestMSE)))
    exportTreesFromRegressionForest(f, bestForest)
    return r_forest

def createRandomForestRegressorAndClassifyData(swedishChildrenList, israeliChildrenList, printFlag = True):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    f, X, c = getDataForClassification(swedishChildrenList, israeliChildrenList)
    #printVectors(f,X)
    #regressionTreeCreator(f, X, c)
    forest = regressionForestCreator(f, X, c) #Full version is with better syntax
    #print("Forest creation time took %i minutes" % (stop_forest_time - start_forest_time))/60

    #classifyData(forest, children)




