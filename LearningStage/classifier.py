
def classifyData(forest, children):
    for c in children:
        # TODO fv = getFeatureVector(c)
        predictation = forest.predict(fv)