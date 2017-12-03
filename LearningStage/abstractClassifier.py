from Parser.auxiliary import NA, MONTHS
from Parser.swedishChild import SwedishChild
from Parser.israeliChild import IsraeliChild
from Parser.child import Child
from abc import ABC, abstractmethod
import numpy as np

NO_CLASSIFICATION = 0


# abstract class for all the classifiers
class AbstractClassifier(ABC):

    @abstractmethod
    def __init__(self):
        pass

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
        f_class= []
        X_regress = []
        f_regress = []
        i = 0
        if ch.__class__ == SwedishChild:
            for feature in f:
                if feature in self.swe_classi_f and feature not in f_class:
                    X_class.append(X[i])
                    f_class.append(feature)
                if feature in self.swe_regress_f and feature not in f_regress:
                    X_regress.append(X[i])
                    f_regress.append(feature)
                i += 1
            if X_class.__contains__(np.NaN) or X_regress.__contains__(np.NaN):
                return NA
            return self._predict_swedish(self.fit(X_class), self.fit(X_regress))
        elif ch.__class__ == IsraeliChild:
            for feature in f:
                if feature in self.isr_classi_f and feature not in f_class:
                    X_class.append(X[i])
                    f_class.append(feature)
                if feature in self.isr_regress_f and feature not in f_regress:
                    X_regress.append(X[i])
                    f_regress.append(feature)
                i += 1
            if X_class.__contains__(np.NaN) or X_regress.__contains__(np.NaN):
                return NA
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
