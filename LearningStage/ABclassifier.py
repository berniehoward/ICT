from sklearn.ensemble import AdaBoostClassifier
from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, AdaBoostRegressor
from sklearn.feature_selection import RFE, SelectKBest
from Parser.auxiliary import Nationality
from LearningStage.abstractClassifier import AbstractClassifier


# Black box algorithm for ICT tagging of ISR and SWE children
class AdaBoostAlgorithm(AbstractClassifier):

    def __init__(self, data, isr_class_args, isr_reg_args, swe_class_args, swe_reg_args):
        X_classi_isr, c_classi_isr, isr_classi_f, X_regress_isr, c_regress_isr, isr_regress_f, X_classi_swe, \
        c_classi_swe, swe_classi_f, X_regress_swe, c_regress_swe, swe_regress_f = data
        self.isr_classificator,  self.isr_classi_f = self.createAB(X_classi_isr, c_classi_isr, isr_class_args,
            RandomForestClassifier, AdaBoostClassifier, Nationality.ISR, isr_classi_f)
        self.swe_classificator, self.swe_classi_f = self.createAB(X_classi_swe, c_classi_swe, swe_class_args,
            RandomForestClassifier, AdaBoostClassifier, Nationality.SWE, swe_classi_f)
        self.isr_regressor, self.isr_regress_f = self.createAB(X_regress_isr, c_regress_isr, isr_reg_args,
            RandomForestRegressor, AdaBoostRegressor, Nationality.ISR, isr_regress_f)
        self.swe_regressor, self.swe_regress_f = self.createAB(X_regress_swe, c_regress_swe, swe_reg_args,
            RandomForestRegressor, AdaBoostRegressor, Nationality.SWE, swe_regress_f)

    def createAB(self, X, c, args, forestType, abType, nationaliity, f):
        imputer = Imputer(strategy='median', axis=0)
        X = imputer.fit_transform(X)

        if len(args) == 7:
            K, N_ES, N, P, D, L, S = args
        else:
            K, N_ES, N, P, D, L = args
            S = 2  # default value

        r_forest = forestType(max_depth=D, max_features=P, random_state=1, min_samples_split=S,
                              min_samples_leaf=L, n_estimators=N)
        AB = abType(base_estimator=r_forest, n_estimators=N_ES, random_state=1)
        AB.fit(X, c)

        def scoringFunction(X, c):
            AB.fit(X, c)
            return AB.feature_importances_

        if len(set(c)) == 2:  # Classifier
            selector = RFE(AB, K, step=1)
        else:  # Regressor
            if nationaliity == Nationality.ISR:
                selector = RFE(AB, K, step=1)
            else:
                selector = SelectKBest(scoringFunction, k=K)

        new_X = selector.fit_transform(X, c)
        new_f = []
        i = 0
        for b in selector.get_support():
            if b:
                new_f.append(f[i])
            i += 1

        AB.fit(new_X, c)
        return AB, new_f