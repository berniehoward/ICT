# print statistics of different lists of samples
def printSampleListStatistics(isr_children, swe_children):
    goodSamples = []
    goodSamplesWithHC = []
    badSamples = []
    for c in isr_children:
        goodSamples = goodSamples + c.goodSamples
        goodSamplesWithHC = goodSamplesWithHC + c.goodSamplesWithHC
        badSamples = badSamples + c.badSamples
    print("isr sum of goodSamples: = ", len(goodSamples) / len([c for c in isr_children]))
    print("isr sum of goodSamplesWithHC: = ", len(goodSamplesWithHC) / len([c for c in isr_children]))
    print("isr sum of badSamples: = ", len(badSamples) / len([c for c in isr_children]))
    print()

    goodSamples = []
    goodSamplesWithHC = []
    badSamples = []

    for c in swe_children:
        goodSamples = goodSamples + c.goodSamples
        goodSamplesWithHC = goodSamplesWithHC + c.goodSamplesWithHC
        badSamples = badSamples + c.badSamples
    print("swe sum of goodSamples: = ", len(goodSamples) / len([c for c in swe_children]))
    print("swe sum of goodSamplesWithHC: = ", len(goodSamplesWithHC) / len([c for c in swe_children]))
    print("swe sum of badSamples: = ", len(badSamples) / len([c for c in swe_children]))