import numpy as np
from scipy.special import erf


# calculates the integrated Gaussian distribution
def gauss_int(x, max_val, min_val, x0, w, reverse):
    if not reverse:
        return (max_val - min_val) / 2 * (1 + erf(np.sqrt(2) * (x - x0) / w)) + min_val
    else:
        return (max_val - min_val) / 2 * (1 - erf(np.sqrt(2) * (x - x0) / w)) + min_val


# signum function
def sign(x):
    return 1 if x >= 0 else -1
