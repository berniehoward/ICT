from LearningStage.classificationExperiment import createBoolClassification
from LearningStage.regressionExperiment import createRegressionClassification
import os


# Perform the experiment of the third stage
def program(swedishChildrenList, israeliChildrenList):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    createBoolClassification(swedishChildrenList, israeliChildrenList)
    # createRegressionClassification(swedishChildrenList, israeliChildrenList)