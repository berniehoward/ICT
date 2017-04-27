from auxiliary import *
from swedishParsing import *
from israelParsing import *
from dictionary import childrenDictionary


if __name__ == '__main__':
    dictionary = childrenDictionary()
    dictionary.swedishChildren = parseSwedish()
    dictionary.israeliChildren.add(parseIsraeli())