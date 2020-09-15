from lmfit import Model
import numpy as np
from typing import Union

from labhelpers.Analysis.functions import sinc2


def get_fw_at_nth_of_max(x: np.ndarray, y: np.ndarray, n: Union[float, int]) -> float:
    """
    Calculates an estimator for the full width at 1/n of maximum of given distribution.
    :param x: Independent variable.
    :param y: Dependent variable.
    :param n: Fraction of maximum to find width for.
    :return: Estimator for full width for which y >= y_max/n
    """
    if n <= 1:
        raise ValueError("n must be larger than 1.")
    elif np.ndim(x) != 1:
        raise ValueError(f"Array x must be one-dimensional, but has dimension {np.ndim(x)}.")
    elif np.ndim(y) != 1:
        raise ValueError(f"Array y must be one-dimensional, but has dimension {np.ndim(y)}.")
    elif np.size(x) != np.size(y):
        raise ValueError(f"Arrays x and y must be of equal size, but have lengths {np.size(x)} and {np.size(y)}.")
    ix_max = np.argmax(y)
    ymax = y[ix_max]
    for i in range(ix_max, -1, -1):
        if y[i] < ymax / n:
            break
    ix_lower = i
    size = np.size(y)
    for i in range(ix_max, size):
        if y[i] < ymax / n:
            break
    ix_upper = i
    return x[ix_upper] - x[ix_lower]


def _get_fwhm(x: np.ndarray, y: np.ndarray) -> float:
    """
    Calculates an estimator for the FWHM of a given distribution
    :param x: Independent variable.
    :param y: Dependent variable.
    :return: Estimator for FWHM.
    """
    return get_fw_at_nth_of_max(x, y, 2)


class Sinc2Model(Model):
    def __init__(self, x, y):
        super().__init__(sinc2)
        fwhm_factor = 2 * 1.37677  # 1.37677: positive solution to the equation (sin(x)/x)^2 = 1/2
        self.make_params(x0=x[np.argmax(y)],
                         a=np.max(y) - np.min(y),
                         b=fwhm_factor / _get_fwhm(x, y),
                         y0=np.min(y))
