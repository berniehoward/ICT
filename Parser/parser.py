from Parser.dictionary import childrenDictionary

def print_sample_statistics(t, missing):
    avg_s, min_s, max_s, hist = childrenDictionary.getStatisticsOfSampls(t, missing)
    print("Average number of sampls is : " + str(avg_s))
    print("Min number of sampls is : " + str(min_s))
    print("Max number of sampls is : " + str(max_s))
    string_hist = ', '.join(str(i) for i in hist)
    print("Histogram: " + string_hist)

def print_statistics(t):
    if t == "S":
        string = "swedish"
    else:
        string = "israeli"
    print("Number of " + string + " children is: " + str(childrenDictionary.getNumOfchildren(t)))
    print()
    print("############# Full sampls ################")
    print_sample_statistics(t, False)
    print()
    print("############# Missing sampls ################")
    print_sample_statistics(t, True)


