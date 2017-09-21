from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import KFold
from Parser.auxiliary import NA
from Parser.swedishChild import SwedishChild
from Parser.israeliChild import IsraeliChild
import numpy as np

NO_CLASSIFICATION = 0

class LearningAlgorithm():

    def __init__(self, data, isr_class_args, isr_reg_args, swe_class_args, swe_reg_args):
        X, c = data
        self.isr_classificator = self.createForest(X, c, isr_class_args, RandomForestClassifier)
        self.swe_classificator = self.createForest(X, c, swe_class_args, RandomForestClassifier)
        self.isr_regressor = self.createForest(X, c, isr_reg_args, RandomForestRegressor)
        self.swe_regressor = self.createForest(X, c, swe_reg_args, RandomForestRegressor)

    def createForest(self, X, c, args, forestType):
        crossvalidation = KFold(n_splits=10, shuffle=True, random_state=1)
        imputer = Imputer(strategy='median', axis=0)
        if len(args) == 5:
            N, P, D, L, S = args
        else:
            N, P, D, L = args
            S = 2  # default value
        X = imputer.fit_transform(X)
        r_forest = forestType(max_depth=D, max_features=P, random_state=1, min_samples_split=S,
                                          min_samples_leaf=L, n_estimators=N)
        r_forest.fit(X, c)
        return r_forest

    def classifyChild(self, forest, ch):
        if len(ch.goodSamples) == 0:
            return NA

        if ch.__class__ == SwedishChild:
            common_ages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 1.0]
        else:
            common_ages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
        f, X, c = ch.generateParametersForRegressionDecisionTree(common_ages, False)

        if ch.__class__ == SwedishChild:
            return self._predict_swedish(X)
        elif ch.__class__ == IsraeliChild:
            return self._predict_israeli(X)

    def _predict_swedish(self, X):
        if self.swe_classificator.predict(X) != NO_CLASSIFICATION:
            return self.swe_regressor(X)
        return NA

    def _predict_israeli(self, X):
        if self.isr_classificator.predict(X) != NO_CLASSIFICATION:
            return self.isr_regressor(X)
        return NA