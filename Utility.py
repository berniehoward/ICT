import numpy as np


# Return the index of the element at the array which is the nearest to value
def find_nearest(array, value):
    idx = (np.abs([x-value for x in array])).argmin()
    return idx
