from builtins import KeyboardInterrupt
import os, csv, sys
import pickle as pkl
from Parser.auxiliary import Nationality, NA
from Parser.swedishChild import SwedishChild
from Parser.israeliChild import IsraeliChild
classifier_path = lambda file: os.path.join(os.getcwd(), file)

swe_common_ages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 1.0]
isr_common_ages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
SINGLE_CHILD = 2

def classify_single_child(classifier, final_classifier, isUniversal, accuracyFlag):
    samples = []
    try:
        while True:
            print("Please insert Origin (0 for ISR, 1 for SWE), child's age (M), length (CM), weight (KG) and Head Circumference (CM) seprated by spaces.")
            print("break with ctrl+c")
            sample_input = input()
            if len(sample_input.split()) != 4:
                print("Bad sample")
                continue
            sample = [float(x) for x in sample_input.split()]
            if all(sample):
                samples.append(sample)
            else:
                print("Bad sample")
    except KeyboardInterrupt:
        c = None #TODO: create child instance
        # final_classifier.classifyChild(c)
        pass

def classify_csv_file(samples, final_classifier, isUniversal, accuracyFlag):
    children = list(set([s[0] for s in samples]))
    print(children)
    for ch in children:
        ch_s = [s[1:] for s in samples if s[0] == ch]
        origin = ch_s[0][0]
        if int(origin) == Nationality.SWE.value :
            c = SwedishChild(int(ch), NA, NA, NA, NA, NA, NA, NA, NA)
            for x in ch_s:
                fs = [float(i) for i in x[1:4]]
                c.addSample(sum([[0],fs], []))
            c.setPretermFlag()
            c.calculateSlops()
            c.calculateBurst()
            c.setValuesOfSlopeVectors()
            x = final_classifier.classifyChild(c)
            print(x)
        else:
            c = IsraeliChild(int(ch), NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA)
            for x in ch_s:
                fs = [float(i) for i in x[1:5]]
                c.addSample(fs)
            c.setPretermFlag()
            c.calculateSlops()
            c.calculateBurst()
            c.setValuesOfSlopeVectors()
            x = final_classifier.classifyChild(c)
            print(x)
    pass

if __name__ == '__main__':
    with open(sys.argv[1], "rb") as pklfile:
        final_classifier = pkl.load(pklfile)

    print("Welcome to the ICT Classifier!\nPlease follow the instructions below\n\n")
    print("NOTICE!!! this version is not comaptible with vectors with missing elements. Use with caution.\n")
    isUniversal = input("Insert type:\n\t1 for the universal classifier\n\t2 for regular (origin-related classifier)\n")
    accuracyFlag = input("Insert accuracy:\n\t1 for accurate classifier\n\t2 for fast classifier\n")
    method = input("Insert insertion Method: \n\t1 in order to classify a csv file \n\t2 for a single classification\n")

    if int(method) == SINGLE_CHILD:
        classify_single_child(final_classifier, isUniversal, accuracyFlag)
    else:
        csvpath = input("Please insert csv file path, filled exactly like the example file\n")
        with open(csvpath, 'r') as f:
            ch = list(csv.reader(f))
        classify_csv_file(ch[1:], final_classifier, isUniversal, accuracyFlag)