from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import Imputer
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from simpleai.search.local import hill_climbing
from LearningStage.parametersTuningLocalSearch import ParametersTuningLocalSearch
from LearningStage.utility import printVectors
from LearningStage.expProg import determineRanges


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
def booleanTreesExp(is_f, is_X, is_c, sw_f, sw_X, sw_c, mix_f, mix_X, mix_c, flag):
    print("Israeli ranges: ")
    determineRanges(is_f, is_X, is_c, randomForestCreator)
    print("Swedish ranges: ")
    determineRanges(sw_f, sw_X, sw_c, randomForestCreator)
    print("Mix ranges: ")
    determineRanges(mix_f, mix_X, mix_c, randomForestCreator)