from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import KFold
from Parser.auxiliary import NA, MONTHS
from Parser.swedishChild import SwedishChild
from Parser.israeliChild import IsraeliChild
from Parser.child import Child
from sklearn.feature_selection import RFE, SelectKBest
import numpy as np

NO_CLASSIFICATION = 0

# Black box algorithm for ICT tagging of ISR and SWE children
class RandomForestAlgorithm:

    def __init__(self, data, isr_class_args, isr_reg_args, swe_class_args, swe_reg_args):
        X_classi_isr, c_classi_isr, isr_classi_f, X_regress_isr, c_regress_isr, isr_regress_f, X_classi_swe, \
        c_classi_swe, swe_classi_f, X_regress_swe, c_regress_swe, swe_regress_f = data
        self.isr_classificator,  self.isr_classi_f = self.createForest(X_classi_isr, c_classi_isr, isr_class_args,
                                                                       RandomForestClassifier, isr_classi_f)
        self.swe_classificator, self.swe_classi_f = self.createForest(X_classi_swe, c_classi_swe, swe_class_args,
                                                                      RandomForestClassifier, swe_classi_f)
        self.isr_regressor, self.isr_regress_f = self.createForest(X_regress_isr, c_regress_isr, isr_reg_args,
                                                                   RandomForestRegressor, isr_regress_f)
        self.swe_regressor, self.swe_regress_f = self.createForest(X_regress_swe, c_regress_swe, swe_reg_args,
                                                                   RandomForestRegressor, swe_regress_f)

    def createForest(self, X, c, args, forestType, f):
        imputer = Imputer(strategy='median', axis=0)
        if len(args) == 6:
            N, P, D, L, S, K = args
        else:
            N, P, D, L, K = args
            S = 2  # default value
        X = imputer.fit_transform(X)
        r_forest = forestType(max_depth=D, max_features=P, random_state=1, min_samples_split=S,
                              min_samples_leaf=L, n_estimators=N)
        r_forest.fit(X, c)

        def scoringFunction(X, c):
            r_forest.fit(X, c)
            return r_forest.feature_importances_

        if len(set(c)) == 2:  # Classifier
            selector = SelectKBest(scoringFunction, k=K)
        else:  # Regressor
            selector = RFE(r_forest, K, step=1)

        new_X = selector.fit_transform(X, c)
        new_f = []
        i = 0
        for b in selector.get_support():
            if b:
                new_f.append(f[i])
            i += 1

        r_forest.fit(new_X, c)
        return r_forest, new_f

    def classifyIsrBySwe(self, ch):
        if len(ch.goodSamples) == 0:
            return NA

        if ch.__class__ == SwedishChild:
            common_ages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 1.0]
        else:
            common_ages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]

        ch.__class__ = Child
        f, X, c = ch.generateParametersForRegressionDecisionTree(common_ages, False)
        X_class = []
        X_regress = []
        i = 0
        if ch.__class__ == Child:
            for feature in f:
                if feature in self.swe_classi_f:
                    X_class.append(X[i])
                if feature in self.swe_regress_f:
                    X_regress.append(X[i])
                i += 1
            return self._predict_swedish(self.fit(X_class), self.fit(X_regress))

    def classifyChild(self, ch):
        if len(ch.goodSamples) == 0:
            return NA

        if ch.__class__ == SwedishChild:
            common_ages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 1.0]
        else:
            common_ages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]

        f, X, c = ch.generateParametersForRegressionDecisionTree(common_ages, False)
        X_class = []
        X_regress = []
        i = 0
        if ch.__class__ == SwedishChild:
            for feature in f:
                if feature in self.swe_classi_f:
                    X_class.append(X[i])
                if feature in self.swe_regress_f:
                    X_regress.append(X[i])
                i += 1
            return self._predict_swedish(self.fit(X_class), self.fit(X_regress))
        elif ch.__class__ == IsraeliChild:
            for feature in f:
                if feature in self.isr_classi_f:
                    X_class.append(X[i])
                if feature in self.isr_regress_f:
                    X_regress.append(X[i])
                i += 1
            return self._predict_israeli(self.fit(X_class), self.fit(X_regress))

    def _predict_swedish(self, X_class, X_regress):
        if self.swe_classificator.predict(X_class) != NO_CLASSIFICATION:
            if X_regress is None:
                return NA
            return self.swe_regressor.predict(X_regress)[0] * MONTHS
        return NA

    def _predict_israeli(self, X_class, X_regress):
        if self.isr_classificator.predict(X_class) != NO_CLASSIFICATION:
            if X_regress is None:
                return NA
            return self.isr_regressor.predict(X_regress)[0] * MONTHS
        return NA

    def fit(self, X):
        for f in X:
            if f is np.NAN:
                return None  # The child doesn't have all the feature
        X = np.asarray(X)
        return X.reshape(1, -1)
