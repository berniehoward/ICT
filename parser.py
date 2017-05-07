from auxiliary import *
from swedishParsing import *
from israelParsing import *
from dictionary import childrenDictionary


if __name__ == '__main__':
    dictionary = childrenDictionary()
    dictionary.swedishChildren = parseSwedish()
    print("Number of swedish children is: " + str(dictionary.getNumOfchildren("S")))
    print()
    avg_s, min_s, max_s, hist = dictionary.getNumOfSwedishSampls()
    print("############# Full sampls ################")
    print("Average number of full sampls is : " + str(avg_s))
    print("Min number of full sampls is : " + str(min_s))
    print("Max number of full sampls is : " + str(max_s))
    string_hist = ', '.join(str(i) for i in hist)
    print("Histogram: " + string_hist)
    avg_s, min_s, max_s, hist = dictionary.getNumOfSwedishSampls(True)
    print()
    print("############# Missing sampls ################")
    print("Average number of missing sampls is : " + str(avg_s))
    print("Min number of missing sampls is : " + str(min_s))
    print("Max number of missing sampls is : " + str(max_s))
    string_hist = ', '.join(str(i) for i in hist)
    print("Histogram: " + string_hist)
    dictionary.israeliChildren.add(parseIsraeli())
    print("Number of israeli children is: " + str(dictionary.getNumOfchildren("I")))