import numpy as np


def find_nearest(array, value):
    idx = (np.abs([x-value for x in array])).argmin()
    return idx

