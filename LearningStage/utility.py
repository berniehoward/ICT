from numpy import around
from collections import Counter
from Parser.child import Child
from Parser.auxiliary import Gender, Nationality
from sklearn.tree import export_graphviz
from pydotplus import graph_from_dot_data
from sklearn import tree
from enum import Enum
import six, os, time, itertools

randomforestpath = lambda file: os.path.join(os.getcwd(), "LearningStage", file)
PICKLE_RANDOM_FOREST_FILE = 'RandomForestAlgorithm.pkl'


class DecisionAlgorithmType(Enum):
    CLASSIFICATION = 0
    REGRESSION = 1
    ADABOOST = 2


def getTenMostCommonAges(children, n):
    allSamples = []
    for x in children:
        allSamples.append(x.goodSamples)

    allSamples = sum(allSamples, [])  # flatten list
    r = [float(format(around(x.age, 1), '.2f')) for x in allSamples]

    return [x[0] for x in Counter(r).most_common(n)]


# print (feature, value) aux function
def printVectors(f, X):
    for x in X:
        print("feature number:", len(x),[(fe,x) for fe, x in zip(f,x)])


# merge all children for merged regression or boolean tree
def mergeChildren(israeliChildrenList, swedishChildrenList):
    children = []
    for i in israeliChildrenList:
        i.__class__ = Child
        children.append(i)
    for i in swedishChildrenList:
        i.__class__ = Child
        children.append(i)
    return children


# split children into separate groups by gender
def splitByGender(children):
    males = [i for i in children if i.sex == Gender.MALE.value]
    females = [i for i in children if i.sex == Gender.FEMALE.value]
    return males, females


# remove nation feature for less warnings
def removeNationFeature(X, f):
    i = f.index('nation')
    new_f = f[:i] + f[i + 1:]
    new_X = []
    for x in X:
        new_X.append(x[:i] + x[i + 1:])
    return new_X, new_f


# Export forest into png files
def exportTreesFromForest(f, r_forest, nationality, type):
    cwd = os.getcwd()
    if type == DecisionAlgorithmType.REGRESSION.name:
        rf_path = os.path.join(cwd, "RegressionResults", str(nationality), "RegressionForest")
    else:
        rf_path = os.path.join(cwd, "ClassificationResults", str(nationality), "ClassificationForest")
    os.makedirs(rf_path)
    os.chdir(rf_path)
    for regression_tree in r_forest.estimators_:
            dotfile = six.StringIO()
            tree.export_graphviz(regression_tree, feature_names=f, out_file=dotfile)
            graph_from_dot_data(dotfile.getvalue()).write_png('tree_' + str(r_forest.estimators_.index(regression_tree))
                                                              +'.png')
    os.chdir(cwd)
