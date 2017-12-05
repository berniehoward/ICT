from builtins import KeyboardInterrupt
import os, csv
import pickle as pkl

classifier_path = lambda file: os.path.join(os.getcwd(), file)
FINAL_CLASSIFIER_FILE ='Classifier.pkl'
SINGLE_CHILD = 2

def classify_single_child(classifier):
    samples = []
    try:
        while True:
            print("Please insert child's age (M), length (CM), weight (KG) and Head Circumference (CM) \
            seprated by spaces\n")
            sample_input = input()
            sample = [float(x) for x in sample_input.split()]
            if all(sample):
                samples.append(sample)
            else:
                print("bad sample\n")
    except KeyboardInterrupt:
        c = None #TODO: create child instance
        final_classifier.classifyChild(c)
        pass

def classify_csv_file(csvfile):
    pass

if __name__ == '__main__':
    with open(classifier_path(FINAL_CLASSIFIER_FILE), "rb") as pklfile:
        final_classifier = pkl.load(pklfile)

    print("Welcome to the ICT Classifier!\nPlease follow the instructions below\n\n")
    print("NOTICE!!! this version is not comaptible with vectors with missing elements. Use with caution.\n")
    isUniversal = input("Insert type:\n\t1 for the universal classifier\n\t2 for regular (origin-related classifier)\n")
    accuracyFlag = input("Insert accuracy:\n\t1 for accurate classifier\n\t2 for fast classifier\n")
    method = input("Insert insertion Method: \n\t1 in order to classify a csv file \n\t2 for a single classification\n")
    classifier = final_classifier(isUniversal, accuracyFlag)

    if method == SINGLE_CHILD:
        classify_single_child(classifier)
    else:
        csvpath = input("Please insert csv file path, filled exactly like the example file\n")
        with open(csvpath, 'r') as f:
            ch = list(csv.reader(f))
        classify_csv_file(ch[1:])