from LearningStage.utility import getTenMostCommonAges, mergeChildren
from LearningStage.utility import printVectors
from Parser.auxiliary import NA
from LearningStage.regressionRandomForest import *
import numpy as np
import os


# Return features(list of all the features' names) , data(list of all the features) and
# classifications (list of ICT tags for every child)
def getDataForClassification(children):
    data = []
    classifications = []
    features = []
    common_ages = sorted(getTenMostCommonAges(children, 8))
    for ch in children:
        if len(ch.goodSamples) == 0:
            continue
        f, d, c = ch.generateParametersForRegressionDecisionTree(common_ages, False)
        features = [i for i in f]
        if not c:
            continue
        data.append([x if x != NA else np.NaN for x in d])
        classifications.append(c)
    return features, data, classifications

# Perform the experiment of the third stage
def program(swedishChildrenList ,israeliChildrenList):
    # Get feature vectors and classification
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    # f, X, c = getDataForClassification(israeliChildrenList)
    # determineRanges(f, X, c, regressionForestCreator)
    # f, X, c = getDataForClassification(swedishChildrenList)
    # determineRanges(f, X, c, regressionForestCreator)

    # printVectors(f, X)
    # Binary trees
    # TODO - complete

    allChildren = mergeChildren(israeliChildrenList, swedishChildrenList)
    f, X, c = getDataForClassification(allChildren)

    # Regression trees
    determineRanges(f, X, c, regressionForestCreator)
