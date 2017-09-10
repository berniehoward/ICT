from numpy import around
from collections import Counter
from Parser.child import Child

def getTenMostCommonAges(children, n):
    allSamples = []
    for x in children:
        allSamples.append(x.goodSamples)

    allSamples = sum(allSamples, [])  # flatten list
    r = [float(format(around(x.age, 1), '.2f')) for x in allSamples]

    return [x[0] for x in Counter(r).most_common(n)]

def printVectors(f, X):
    for x in X:
        print("feature number:", len(x),[(fe,x) for fe, x in zip(f,x)])

# merge all children for merged regression tree
def mergeChildren(israeliChildrenList, swedishChildrenList):
    children = []
    for i in israeliChildrenList:
        i.__class__ = Child
        children.append(i)
    for i in swedishChildrenList:
        i.__class__ = Child
        children.append(i)
    return children