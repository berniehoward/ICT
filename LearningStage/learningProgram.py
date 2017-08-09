from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from sklearn import tree
import numpy as np
from Parser.auxiliary import NA

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


def load_paramters(swedishChildrenList, israeliChildrenList, printFlag = True):
    f, X, c = getDataForClassification(swedishChildrenList, israeliChildrenList)
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    for depth in range(1,10):
        imputer = Imputer(strategy='mean', axis=0)
        X = imputer.fit_transform(X) #instead of fit
        regression_tree = tree.DecisionTreeRegressor(max_depth=depth, random_state=0, min_samples_split=30, min_samples_leaf=10)
        regression_tree.fit(X, c)
        tree.export_graphviz(regression_tree, feature_names=f, out_file = 'tree' + str(depth) + '.dot')
        if regression_tree.fit(X, c).tree_.max_depth < depth:
            break
        score = np.mean(cross_val_score(regression_tree, X, c, scoring='neg_mean_squared_error', cv=crossvalidation, n_jobs=1))
        print("Depth: %i MSE: %.3f" % (depth,abs(score)))


