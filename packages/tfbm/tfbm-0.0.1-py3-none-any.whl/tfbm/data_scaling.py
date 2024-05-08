import numpy as np
from sklearn import preprocessing

def normalize_data_min_max(data):
    return (data - np.amin(data)) / (np.amax(data) - np.amin(data))