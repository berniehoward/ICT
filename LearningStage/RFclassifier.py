from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_selection import RFE, SelectKBest
from LearningStage.abstractClassifier import AbstractClassifier


# Black box algorithm for ICT tagging of ISR and SWE children
class RandomForestAlgorithm(AbstractClassifier):

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
