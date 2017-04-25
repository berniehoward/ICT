getpath = lambda file: os.path.join(os.getcwd(),"ICTData",file)
from time import strptime
from israeliChild import IsraeliChild
from operator import itemgetter
import sys,os, csv, math
from auxiliary import *

"""self, id, sex, birthWeight, birthHeight, gestationalAge, ICT_A, ICT_Z, \
                 familyID, birthPosition, fatherAge, motherAge, motherWeight, motherHeight, \
                 birthMonth, birthYear"""


def crossWithSISB(israeliSamples):
    headers = israeliSamples.pop(0)
    

def parseIsraeli():
    with open(getpath(ISRAELI_MAIN_FILE), 'r') as f:
        israeliSamples = list(csv.reader(f))
