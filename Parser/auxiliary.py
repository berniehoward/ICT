import os
from enum import Enum

# Consts
METER = 100
NA = -100  # value representing we are not able to determine the ICT
KILO = 1000
YEAR = 365
BIRTH = 0
MONTHS = 12
FALSE_DATE = '-100/-100/-100'

# Files
SWEDISH_FILE = "Sweden_ICT.csv"
SWEDISH_NEW_BOYS_FILE = 'NewData\\SwedishBoysFile.csv'
SWEDISH_NEW_GIRLS_FILE = 'NewData\\SwedishGirlsFile.csv'
SWEDISH_NEW_GIRLS_P_FILE = 'NewData\\SwedishGirlsParents.csv'
SWEDISH_NEW_BOYS_P_FILE = 'NewData\\SwedishBoysParents.csv'

#################

ISRAELI_MAIN_FILE = "MS_ICT.csv"
ISRAELI_ADDITIONAL_INFO_FILE = "MS_SIBS.csv"
ISRAELI_FMLY_RSRCH_FILE = "ILS_ResearchGroup.csv"
ISRAELI_FMLY_TEST_FILE = "ILS_TestGroup.csv"
ISRAELI_FMLY_ICT_FILE = "ILS_LargeFamiliesICT.csv"
# ISRAELI_FMLY_ICT2_FILE = "ILS_LargeFamiliesICT2.csv"

#################

PICKLE_FILE = "ChildrenParsedData.pkl"

# Lambdas
getGender = lambda g: Gender.MALE.value if g == 'M' else Gender.FEMALE.value
getpath = lambda file: os.path.join(os.getcwd(), "ICTData", file)
picklepath = lambda file: os.path.join(os.getcwd(), "Parser", file)


class Nationality(Enum):
    ISR = 0
    SWE = 1
    MIX = 2

class Gender(Enum):
    MALE = 1
    FEMALE = 2
