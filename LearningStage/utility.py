from numpy import around
from collections import Counter
from Parser.child import Child
from Parser.auxiliary import Gender


def getTenMostCommonAges(children, n):
    allSamples = []
    for x in children:
        allSamples.append(x.goodSamples)

    allSamples = sum(allSamples, [])  # flatten list
    r = [float(format(around(x.age, 1), '.2f')) for x in allSamples]

    return [x[0] for x in Counter(r).most_common(n)]


# print (feature, value) aux function
def printVectors(f, X):
    for x in X:
        print("feature number:", len(x),[(fe,x) for fe, x in zip(f,x)])


# merge all children for merged regression or boolean tree
def mergeChildren(israeliChildrenList, swedishChildrenList):
    children = []
    for i in israeliChildrenList:
        i.__class__ = Child
        children.append(i)
    for i in swedishChildrenList:
        i.__class__ = Child
        children.append(i)
    return children


# split children into separate groups by gender
def splitByGender(children):
    males = [i for i in children if i.sex == Gender.MALE.value]
    females = [i for i in children if i.sex == Gender.FEMALE.value]
    return males, females