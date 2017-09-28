from sklearn.feature_selection import SelectKBest, f_regression, f_classif, RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
from simpleai.search.local import hill_climbing
from LearningStage.parametersTuningLocalSearch import ParametersTuningLocalSearch
from LearningStage.regressionRandomForest import determineRanges
from LearningStage.utility import getTenMostCommonAges, splitByGender, printVectors
from Parser.auxiliary import NA
import numpy as np


# Return data and classification separated by gender:
def seperateGenders(children):
    males, females = splitByGender(children)
    m_f, m_X, m_c = getDataForBooleanClassification(males)
    f_f, f_X, f_c = getDataForBooleanClassification(females)
    return m_f, m_X, m_c, f_f, f_X, f_c


# Create boolean "Random Forest" by given arguments
def randomForestCreator(f, X, c, args):
    crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
    imputer = Imputer(strategy='median', axis=0)
    if len(args) == 5:
        N, P, D, L, S = args
    else:
        N, P, D, L = args
        S = 2  # default value
    X = imputer.fit_transform(X)  # instead of fit
    r_forest = RandomForestClassifier(max_depth=D, max_features=P, random_state=1, min_samples_split=S,
                                     min_samples_leaf=L, n_estimators=N)
    r_forest.fit(X, c)
    score = np.mean(
        cross_val_score(r_forest, X, c, cv=crossvalidation, scoring='neg_mean_squared_error'))
    return r_forest, score


# Perform the experiment for boolean trees:
def booleanTreesExp(f, X, c, experiment):
    print("%s ranges: " % experiment)
    determineRanges(f, X, c, randomForestCreator)


# boolean parameter Tuning
def booleanParametersTuning(f, X, c, function, ranges):
    boolClass = False  # Boolean classification
    hops = [1, 0.05, 1, 5]
    problem = ParametersTuningLocalSearch(ranges, f, X, c, hops, function, boolClass)
    return hill_climbing(problem, 1000).state


# Return features(list of all the features' names) , data(list of all the features) and
# classifications (list of boolean tags - the child has ICT or not)
def getDataForBooleanClassification(children):
    data = []
    classifications = []
    features = []
    common_ages = sorted(getTenMostCommonAges(children, 8))
    for ch in children:
        if len(ch.goodSamples) == 0:
            continue
        f, d, c = ch.generateParametersForRegressionDecisionTree(common_ages, False)
        features = [i for i in f]
        c = 1 if c != 0 else 0
        data.append([x if x != NA else np.NaN for x in d])
        classifications.append(c)
    return features, data, classifications


# Return the recommended classifier
def createFinalClassificationForest(X, c, f, k, forest, printMode=False):
    selector = SelectKBest(f_classif, k=k)
    new_X = selector.fit_transform(X, c)
    selector = selector.fit(X, c)
    new_f = []
    i = 0
    for b in selector.get_support():
        if b:
            new_f.append(f[i])
        i += 1

    if printMode:
        print(k, " best features are: ", new_f)

    forest.fit(new_X, c)
    return new_f, forest