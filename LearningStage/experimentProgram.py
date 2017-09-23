from LearningStage.classificationExperiment import createBoolClassification
from LearningStage.utility import exportTreesFromForest
from LearningStage.regressionExperiment import createRegressionClassification
import os


# Perform the experiment of the third stage
def program(swedishChildrenList, israeliChildrenList, printMode=False):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    #isr_f, isr_classification_RF, swe_f, swe_classification_RF = \
    createBoolClassification(swedishChildrenList, israeliChildrenList)
    #isr_f, isr_regression_RF, swe_f, swe_regression_RF = createRegressionClassification(swedishChildrenList, israeliChildrenList)
    #if printMode:
    #    exportTreesFromForest(isr_f, isr_regression_RF, "Israeli")
    #    exportTreesFromForest(swe_f, swe_regression_RF, "Swedish")