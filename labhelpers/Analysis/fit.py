from lmfit import Model
import numpy as np
from typing import Union, Tuple
import warnings

from labhelpers.Analysis.functions import sinc2


def _get_fw_at_nth_of_max(x: np.ndarray,
                          y: np.ndarray,
                          n: Union[float, int],
                          return_ix: bool = False) -> Union[float, Tuple[int, int]]:
    """
    Calculates an estimator for the full width at 1/n of maximum of given distribution.
    :param x: 1 dimensional numpy array with values of independent variable.
    :param y: 1 dimensional numpy array with values of dependent variable.
    :param n: Fraction of maximum to find width for. Must be larger than one.
    :return: Estimator for full width for which y >= y_max/n
    """
    # check parameters
    if n <= 1:
        raise ValueError("n must be larger than 1.")
    elif np.ndim(x) != 1:
        raise ValueError(f"Array x must be one-dimensional, but has dimension {np.ndim(x)}.")
    elif np.ndim(y) != 1:
        raise ValueError(f"Array y must be one-dimensional, but has dimension {np.ndim(y)}.")
    elif np.size(x) != np.size(y):
        raise ValueError(f"Arrays x and y must be of equal size, but have lengths {np.size(x)} and {np.size(y)}.")
    # find index of maximum value
    ix_max = np.argmax(y)
    if np.size(ix_max) > 1:
        warnings.warn("Values has more than one maximum value. Only take first occurence.", RuntimeWarning)
        ix_max = ix_max[0]
    # find first values for which y < y_max / n
    ymax = y[ix_max]
    ix_lower = ix_max
    ix_upper = ix_max
    for i in range(ix_max, -1, -1):
        if y[i] < ymax / n:
            ix_lower = i
            break
    size = np.size(y)
    for i in range(ix_max, size):
        if y[i] < ymax / n:
            ix_upper = i
            break
    if return_ix:
        return ix_lower, ix_upper
    else:
        return x[ix_upper] - x[ix_lower]


def _get_fwhm(x: np.ndarray, y: np.ndarray, return_ix: bool = False) -> Union[float, Tuple[int, int]]:
    """
    Calculates an estimator for the FWHM of a given distribution
    :param x: Independent variable.
    :param y: Dependent variable.
    :return: Estimator for FWHM.
    """
    return _get_fw_at_nth_of_max(x, y, 2, return_ix)


class Sinc2Model(Model):
    def __init__(self, x, y):
        super().__init__(sinc2)
        fwhm_factor = 2 * 1.37677  # 1.37677: positive solution to the equation (sin(x)/x)^2 = 1/2
        self.fwhm_ix = _get_fwhm(x, y, return_ix=True)
        self.init_guess = {'x0': x[np.argmax(y)],
                           'a': np.max(y) - np.min(y),
                           'b': fwhm_factor / _get_fwhm(x, y),
                           'y0': np.min(y)}
        self.params = self.make_params(**self.init_guess)
        self._fit = self.fit
        self.x = x
        self.y = y

    def do_fit(self, data_range: Tuple[int, int] = None):
        if data_range is None:
            x = self.x
            y = self.y
        else:
            x = self.x[data_range[0]:data_range[1]]
            y = self.y[data_range[0]:data_range[1]]
        self.params['x0'].set(min=np.min(x), max=np.max(x))
        return self.fit(y, self.params, x=x)
