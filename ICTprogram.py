import pickle as pkl

from Parser.auxiliary import picklepath, PICKLE_FILE
from Parser.parsingStage import parsingStage
from SecondStage.FullExperiment import fullProg as secondStage
from SecondStage.automaticTagging import automaticTagging
# from LearningStage.learningProgram import load_paramters as ThirdStage

if __name__ == '__main__':
    # parsingStage()

    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        swedishChildrenList, israeliChildrenList = pkl.load(pklfile)

    # secondStage(swedishChildrenList, israeliChildrenList, True)
    # automaticTagging(swedishChildrenList)
    # automaticTagging(israeliChildrenList)

    # ThirdStage(swedishChildrenList, israeliChildrenList, True)


