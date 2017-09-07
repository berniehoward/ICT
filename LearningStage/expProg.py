from LearningStage.utility import getTenMostCommonAges
from Parser.auxiliary import NA
from LearningStage.regressionRandomForest import determineRanges
import numpy as np


# Return features(list of all the features' names) , data(list of all the features) and
# classifications (list of ICT tags for every child)
def getDataForClassification(children):
    data = []
    classifications = []
    features = []
    checkFlag = False
    common_ages = sorted(getTenMostCommonAges(children, 10))
    for ch in children:
        if len(ch.goodSamples) == 0:
            continue
        f, d, c = ch.generateParametersForRegressionDecisionTree(common_ages, False)
        if not checkFlag:
            features = [i for i in f]
            checkFlag = True
        if not c:
            continue
        data.append([x if x != NA else np.NaN for x in d])
        classifications.append(c)
    return features, data, classifications


# Perform the experiment of the third stage
def program(israeliChildrenList):
    f, X, c = getDataForClassification(israeliChildrenList)
    determineRanges(X, c)