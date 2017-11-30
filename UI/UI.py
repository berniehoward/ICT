from builtins import KeyboardInterrupt

SINGLE_CHILD = 2

def classify_single_child(classifier):
    samples = []
    try:
        while True:
            print("Please insert child's age, length, height, HC seprated by spaces\n")
            print("If one of the element is unknown, leave it empty\n")
            sample_input = input()
            sample = [float(x) for x in sample_input.split()]
            samples.append(sample)
    except KeyboardInterrupt:
        # call classifer with child samples
        pass


def userMain():
    print("Welcome to the ICT Classifier!\nPlease follow the instructions below\n\n")
    isUniversal = input("Insert type:\n\t1 for the universal classifier\n\t2 for regular (origin-related classifier)\n")
    accuracy = input("Insert accuracy:\n\t1 for accurate classifier\n\t2 for fast classifier\n")
    method = input("Insert insertion Method: \n\t1 in order to classify a csv file \n\t2 for a single classification\n")
    if isUniversal == True:
        classifier = None #TODO
    else:
        classifier = None #TODO

    if method == SINGLE_CHILD:
        classify_single_child(classifier)
    else:
        csvpath = input("Please insert csv file path, filled exactly like the example file\n")
        #