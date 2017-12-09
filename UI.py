import os, csv, sys
import pickle as pkl
from Parser.auxiliary import Nationality, NA, MONTHS
from Parser.swedishChild import SwedishChild
from Parser.israeliChild import IsraeliChild
classifier_path = lambda file: os.path.join(os.getcwd(), file)

swe_common_ages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 1.0]
isr_common_ages = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8]
SINGLE_CHILD = 2
ACCURATE = 1
def classify(ch, samples, final_classifier, isUniversal, accuracyFlag):
    origin = samples[0][0]
    birth = samples[0]
    bm = input("Please enter child birth month\n")
    if int(origin) == Nationality.SWE.value or isUniversal == 2:
        if birth[1] == 0:
            c = SwedishChild(int(ch), NA, birth[1], NA, NA, NA, NA, NA, int(bm))
        else:
            c = SwedishChild(int(ch), NA, NA, NA, NA, NA, NA, NA, NA)
        for x in samples:
            fs = [float(i) for i in x[1:4]]
            c.addSample([0] + [fs[0] / MONTHS] + [fs[1]] + [fs[2]])
        c.setPretermFlag()
        c.calculateSlops()
        c.calculateBurst()
        c.setValuesOfSlopeVectors()
        return final_classifier.classifyChild(c, accuracyFlag)
    else:
        if birth[1] == 0:
            c = IsraeliChild(int(ch), NA, birth[1], NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, int(bm))
        else:
            c = IsraeliChild(int(ch), NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA)
        for x in samples:
            fs = [float(i) for i in x[1:5]]
            c.addSample(fs)
        c.setPretermFlag()
        c.calculateSlops()
        c.calculateBurst()
        c.setValuesOfSlopeVectors()
        return final_classifier.classifyChild(c, accuracyFlag)

def classify_single_child(final_classifier, isUniversal, accuracyFlag):
    samples = []
    while True:
        print("Please insert Origin (0 for ISR, 1 for SWE), child's age (M), length (CM), weight (KG) and Head Circumference (CM) (if child is israeli). seprated by spaces.")
        print("If you want a fast prediction, insert samples at birth, 1.2, 2.4 and 3.6 months. break with Enter")
        sample_input = input()
        if sample_input == '':
            print("AAA")
            x = classify(0, samples, final_classifier, isUniversal, accuracyFlag)
            print("Prdiected ICT is", x)
            return
        if len(sample_input.split()) != 5:
            print("Bad sample")
            continue
        sample = [float(x) for x in sample_input.split()]
        if '' not in sample:
            samples.append(sample)
        else:
            print("Bad sample")



def classify_csv_file(samples, final_classifier, isUniversal,):
    children = sorted(list(set([s[0] for s in samples])))
    for ch in children:
        ch_s = [s[1:] for s in samples if s[0] == ch]
        x = classify(ch, ch_s , final_classifier, isUniversal, ACCURATE)
        print("Prdiected ICT of child", int(ch), "is", x)

if __name__ == '__main__':
    with open(sys.argv[1], "rb") as pklfile:
        final_classifier = pkl.load(pklfile)

    print("Welcome to the ICT Classifier!\nPlease follow the instructions below\n\n")
    print("NOTICE!!! this version is not compatible with vectors with missing elements. Use with caution.\n")
    isUniversal = input("Insert type:\n\t1 for the universal classifier\n\t2 for regular (origin-related classifier)\n")
    accuracyFlag = input("Insert accuracy:\n\t1 for accurate classifier\n\t2 for fast classifier\n")
    accuracyFlag = int(accuracyFlag)
    method = input("Insert insertion Method: \n\t1 in order to classify a csv file \n\t2 for a single classification\n")

    if int(method) == SINGLE_CHILD:
        classify_single_child(final_classifier, int(isUniversal), int(accuracyFlag))
    else:
        csvpath = input("Please insert csv file path, filled exactly like the example file\n")
        with open(csvpath, 'r') as f:
            ch = list(csv.reader(f))
        classify_csv_file(ch[1:], final_classifier, int(isUniversal))