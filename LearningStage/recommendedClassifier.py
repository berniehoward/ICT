from sklearn.ensemble import AdaBoostClassifier
from sklearn.preprocessing import Imputer
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, AdaBoostRegressor
from sklearn.feature_selection import RFE
from Parser.auxiliary import Nationality
from LearningStage.abstractClassifier import AbstractClassifier


# Black box algorithm for ICT tagging of ISR and SWE children
class RecommendedAlgorithm(AbstractClassifier):

    def __init__(self, data, isr_class_args, isr_reg_args, swe_class_args, swe_reg_args):
        X_classi_isr, c_classi_isr, isr_classi_f, X_regress_isr, c_regress_isr, isr_regress_f, X_classi_swe, \
        c_classi_swe, swe_classi_f, X_regress_swe, c_regress_swe, swe_regress_f = data

        self.isr_classificator, self.acc_isr_classi_f = \
            self.createClassifier(X_classi_isr, c_classi_isr, isr_class_args, RandomForestClassifier,
                                  AdaBoostClassifier, Nationality.ISR, isr_classi_f)
        self.swe_classificator, self.acc_swe_classi_f = \
            self.createClassifier(X_classi_swe, c_classi_swe, swe_class_args, RandomForestClassifier,
                                  AdaBoostClassifier, Nationality.SWE, swe_classi_f)
        self.isr_regressor, self.acc_isr_regress_f = \
            self.createClassifier(X_regress_isr, c_regress_isr, isr_reg_args, RandomForestRegressor,
                                  AdaBoostRegressor, Nationality.ISR, isr_regress_f)
        self.swe_regressor, self.acc_swe_regress_f = \
            self.createClassifier(X_regress_swe, c_regress_swe, swe_reg_args, RandomForestRegressor,
                                  AdaBoostRegressor, Nationality.SWE, swe_regress_f)

        # Will be completed by different function
        self.fast_isr_classi_f = None
        self.fast_swe_classi_f = None
        self.fast_isr_regress_f = None
        self.fast_swe_regress_f = None

        # Will be completed by the relevant flag while classifying child
        self.isr_classi_f = None
        self.swe_classi_f = None
        self.isr_regress_f = None
        self.swe_regress_f = None

    def addFastOption(self, fast_f):
        fast_isr_classi_f, fast_swe_classi_f, fast_isr_regress_f, fast_swe_regress_f = fast_f
        self.fast_isr_classi_f = fast_isr_classi_f
        self.fast_swe_classi_f = fast_swe_classi_f
        self.fast_isr_regress_f = fast_isr_regress_f
        self.fast_swe_regress_f = fast_swe_regress_f

    def createClassifier(self, X, c, args, forestType, abType, nationaliity, f):
        imputer = Imputer(strategy='median', axis=0)
        X = imputer.fit_transform(X)

        if len(args) == 7:
            K, N_ES, N, P, D, L, S = args
        else:
            K, N_ES, N, P, D, L = args
            S = 2  # default value

        r_forest = forestType(max_depth=D, max_features=P, random_state=1, min_samples_split=S,
                              min_samples_leaf=L, n_estimators=N)
        if N_ES != -1:
            AB = abType(base_estimator=r_forest, n_estimators=N_ES, random_state=1)

        if len(set(c)) == 2:  # Classifier
            selector = RFE(AB, K, step=1)
            classifier = AB
        else:  # Regressor
            if nationaliity == Nationality.ISR:
                classifier = AB
            else:
                classifier = r_forest
            selector = RFE(classifier, K, step=1)
        classifier.fit(X, c)
        new_X = selector.fit_transform(X, c)
        new_f = []
        i = 0
        for b in selector.get_support():
            if b:
                new_f.append(f[i])
            i += 1

        classifier.fit(new_X, c)
        return classifier, new_f

    def getIsClassi(self):
        return self.isr_classificator

    def getIsRegrassor(self):
        return self.isr_regressor

    def getSwClassi(self):
        return self.swe_classificator

    def getSwRegrassor(self):
        return self.swe_regressor

    def getFastIsClassiF(self):
        return self.fast_isr_classi_f

    def getFastISRegF(self):
        return self.fast_isr_regress_f

    def getFastSwClassiF(self):
        return self.fast_swe_classi_f

    def getFastSwRegF(self):
        return self.fast_swe_regress_f

    def classifyChild(self, ch, flag):
        if flag == 1:  # Accuracy
            self.isr_classi_f = self.acc_isr_classi_f
            self.swe_classi_f = self.acc_swe_classi_f
            self.isr_regress_f = self.acc_isr_regress_f
            self.swe_regress_f = self.acc_swe_regress_f

        else:  # Fast
            self.isr_classi_f = self.fast_isr_classi_f
            self.swe_classi_f = self.fast_swe_classi_f
            self.isr_regress_f = self.fast_isr_regress_f
            self.swe_regress_f = self.fast_swe_regress_f

        return AbstractClassifier.classifyChild(self, ch)


