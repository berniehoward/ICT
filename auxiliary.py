import os

#consts

SWEDISH_FILE = "Sweden_ICT.csv"
ISRAELI_MAIN_FILE = "MS_ICT.csv"
METER = 100
NA = -100  # value representing we are not able to determine the ICT


getGender = lambda g: 1 if g == 'M' else 2
getpath = lambda file: os.path.join(os.getcwd(),"ICTData",file)
