
def print_sample_statistics(dictionary, t, missing):
    avg_s, min_s, max_s, hist = dictionary.getStatisticsOfSampls(t, missing)
    print("Average number of sampls is : " + str(avg_s))
    print("Min number of sampls is : " + str(min_s))
    print("Max number of sampls is : " + str(max_s))
    string_hist = ', '.join(str(i) for i in hist)
    print("Histogram: " + string_hist)


def print_statistics(dictionary, t):
    if t == "S":
        string = "swedish"
    else:
        string = "israeli"
    print("Number of " + string + " children is: " + str(dictionary.getNumOfchildren(t)))
    print()
    print("############# Full sampls ################")
    print_sample_statistics(dictionary, t, False)
    print()
    print("############# Missing sampls ################")
    print_sample_statistics(dictionary, t, True)


