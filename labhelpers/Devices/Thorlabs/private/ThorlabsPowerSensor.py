from typing import Union, Dict
import numpy as np

Num = Union[int, float]


class _ThorlabsPowerSensor:
    def __init__(self, linearity_err: Num, calibration_err: Dict[int, float], wvl_range, ureg):
        self._ureg = ureg
        self._err_types = ['linearity', 'calibration']
        self._linearity_err = linearity_err
        self._calibration_err = calibration_err
        self._wvl_min = wvl_range[0]
        self._wvl_max = wvl_range[1]

    def get_error(self, err_type, power, wvl=None):
        if err_type not in self._err_types:
            raise ValueError("Unknown error type.")
        if err_type == self._err_types[0]:
            return power * self._linearity_err
        else:
            if wvl < self._wvl_min or wvl > self._wvl_max:
                raise ValueError("Wavelength out of range.")
            if wvl is None:
                raise ValueError("Wavelength must not be None for calibration error.")
            arr = np.array(list(self._calibration_err.keys())) * self._ureg.nanometer
            return power * self._calibration_err[(arr[np.argmax(arr > wvl) - 1]).to(self._ureg.nanometer).magnitude]
