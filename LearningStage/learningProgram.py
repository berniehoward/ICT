from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold
from sklearn.tree import export_graphviz
from pydotplus import graph_from_dot_data
import six, os, glob
from sklearn.preprocessing import Imputer
from sklearn import tree
import numpy as np
from Parser.auxiliary import NA


"""  
http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html#sklearn.ensemble.RandomForestRegressor
"""

def getDataForClassification(swedishChildrenList, israeliChildrenList):
    data = []
    classifications = []
    features = []
    checkFlag = False
    for c in israeliChildrenList:
        if len(c.id) == 2:
            if len(c.goodSamples) == 0:
                continue
            f, d, c = c.generateParametersForRegressionDecisionTree(True)
            if not checkFlag:
                features = [i for i in f]
            if not c:
                continue
            data.append([x if x!=NA else np.NaN for x in d])
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
    for f in glob.glob('rf_path\*'):
        os.remove(f)
    os.chdir(rf_path)
    for regression_tree in r_forest.estimators_:
            dotfile = six.StringIO()
            tree.export_graphviz(regression_tree, feature_names=f, out_file=dotfile)
            graph_from_dot_data(dotfile.getvalue()).write_png('tree_' + str(r_forest.estimators_.index(regression_tree))
            +'.png')

# If depth == None, then nodes are expanded until all leaves are pure or until all leaves contain less than min_samples_split samples.
def regressionForestCreatorAux(f, X, c, msl, m):
    crossvalidation = KFold(n_splits=2, shuffle=True, random_state=1)
    imputer = Imputer(strategy='mean', axis=0)
    X = imputer.fit_transform(X)  # instead of fit
    r_forest = RandomForestRegressor(max_depth=None, max_features=m, random_state=1,
                                     min_samples_split = 30, min_samples_leaf = msl)
    r_forest.fit(X, c)
    score = np.mean(
        cross_val_score(r_forest, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return r_forest, score

def regressionForestCreator(f, X, c):
    bestForest, best_m, best_msl, bestMSE = None, 0, 0, 1.0
    for msl in range(3, 25):
        for m in [x/100 for x in range(50,100,5)]:
            r_forest, score = regressionForestCreatorAux(f, X, c, msl, m)
            if abs(score) < bestMSE:
                bestForest, best_m, best_msl, bestMSE = r_forest, m, msl, abs(score)
    print("Min Samples In Leaf: %i, max_features: %.2f precent, MSE: %.3f" % (best_msl, best_m, abs(bestMSE)))
    exportTreesFromRegressionForest(f, bestForest)
    return r_forest

def classifyData(forest, children):
    for c in children:
        #TODO fv = getFeatureVector(c)
        predictation = forest.predict(fv)

def createRandomForestRegressorAndClassifyData(swedishChildrenList, israeliChildrenList, printFlag = True):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'
    f, X, c = getDataForClassification(swedishChildrenList, israeliChildrenList)
    #regressionTreeCreator(f, X, c)
    #print()
    forest = regressionForestCreator(f, X, c)
    #classifyData(forest, children)




