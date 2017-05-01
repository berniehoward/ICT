import os

#consts
METER = 100
NA = -100  # value representing we are not able to determine the ICT
KILO = 1000
FALSE_DATE = '1/1/'+ str(NA)

#Files
SWEDISH_FILE = "Sweden_ICT.csv"
ISRAELI_MAIN_FILE = "MS_ICT.csv"
ISRAELI_ADDITIONAL_INFO_FILE = "MS_SIBS.csv"

#lambdas
getGender = lambda g: 1 if g == 'M' else 2
getpath = lambda file: os.path.join(os.getcwd(),"ICTData",file)
