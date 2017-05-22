
import pickle as pkl
from Parser.dictionary import childrenDictionary
from Parser.swedishParsing import parseSwedish
from Parser.israelParsing import parseIsraeli
from Parser.auxiliary import picklepath, PICKLE_FILE
from FirstStage.program import program as firstStage


if __name__ == '__main__':
    dictionary = childrenDictionary()
    dictionary.swedishChildren = parseSwedish()
    #print_statistics("S")
    #print()
    dictionary.israeliChildren = parseIsraeli()
    #print_statistics("I")
    for c in dictionary.swedishChildren:
        print([i.age for i in c.goodSamples])
    with open(picklepath(PICKLE_FILE),"wb") as pklfile:
        pkl.dump(dictionary, pklfile)


"""if __name__ == '__main__':
    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        dictionary = pkl.load(pklfile)
    firstStage(dictionary)"""
