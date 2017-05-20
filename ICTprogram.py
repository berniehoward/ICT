from Parser.dictionary import childrenDictionary
from Parser.swedishParsing import parseSwedish
from Parser.israelParsing import parseIsraeli
import pickle as pkl
from Parser.auxiliary import picklepath, PICKLE_FILE, YEAR, MONTHS, NA
import numpy as np
from scipy import stats

"""if __name__ == '__main__':
    dictionary = childrenDictionary()
    dictionary.swedishChildren = parseSwedish()
    #print_statistics("S")
    #print()
    dictionary.israeliChildren = parseIsraeli()
    #print_statistics("I")
    for c in dictionary.israeliChildren:
        print("goodSamples:",len(c.goodSamples))
    with open(picklepath(PICKLE_FILE),"wb") as pklfile:
        pkl.dump(dictionary, pklfile)"""

def find_nearest(array,value):
    idx = (np.abs([x-value for x in array])).argmin()
    return idx

AGE = 6.5
if __name__ == '__main__':
    with open(picklepath(PICKLE_FILE), "rb") as pklfile:
        dictionary = pkl.load(pklfile)
        
    l = []
    children = []
    for child in list(dictionary.swedishChildren):
        child.calculateBurst()
        i = find_nearest([a.age/YEAR for a in child.goodSamples], AGE)
        #print(child.goodSamples[i].age/YEAR)
        if abs(child.goodSamples[i].age/YEAR - AGE) < 1.0:
            l.append(child.goodSamples[i].height)
            children.append(child)
    norml = stats.zscore(l)
    #print(norml, np.mean(norml))
    g1 = []
    g2 = []
    g3 = []
    for x, y in zip(norml, children):
        print(x,y)
    for x,y in zip(norml, children):
        if x<-0.5:
            g1.append(y)
        elif -0.5<=x<=0.5:
            g2.append(y)
        else:
            g3.append(y)
    print(len(g1),len(g2),len(g3))

    def findNaiveICT(e,child):
        for midage, slope in child.calculateBurst:
            if slope > e:
                return midage
        return NA
    
    epsilons = [] #naive sol
    for e in epsilons:
        icts = [findNaiveICT(e,c) for c in children]
        for x, y in zip(icts, children):
            if x < 8/MONTHS:
                g1.append(y)
            elif 8/MONTHS <= x <= 12/MONTHS:
                g2.append(y)
            else:
                g3.append(y)
        print(len(g1), len(g2), len(g3))