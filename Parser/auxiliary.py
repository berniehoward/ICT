import os

# Consts
METER = 100
NA = -100  # value representing we are not able to determine the ICT
KILO = 1000
YEAR = 365
MONTHS = 12
FALSE_DATE = '1/1/'+ str(NA)

# Files
SWEDISH_FILE = "Sweden_ICT.csv"
ISRAELI_MAIN_FILE = "MS_ICT.csv"
ISRAELI_ADDITIONAL_INFO_FILE = "MS_SIBS.csv"
PICKLE_FILE = "ChildrenSet.pkl"

# Lambdas
getGender = lambda g: 1 if g == 'M' else 2
getpath = lambda file: os.path.join(os.getcwd(),"ICTData",file)
picklepath = lambda file: os.path.join(os.getcwd(),"Parser",file)