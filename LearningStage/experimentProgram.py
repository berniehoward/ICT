from LearningStage.classificationExperiment import createBoolClassification
from LearningStage.utility import exportTreesFromRegressionForest
from LearningStage.regressionExperiment import createRegressionClassification
import os


# Perform the experiment of the third stage
def program(swedishChildrenList, israeliChildrenList, printMode=False):
    os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'  # for plotting trees
    # createBoolClassification(swedishChildrenList, israeliChildrenList)
    is_f, is_final_RF, sw_f, sw_final_RF = createRegressionClassification(swedishChildrenList, israeliChildrenList)
    if printMode:
        exportTreesFromRegressionForest(is_f, is_final_RF, "Israeli")
        exportTreesFromRegressionForest(sw_f, sw_final_RF, "Swedish")