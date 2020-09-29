import numpy as np
import pint


class Crystal:
    def __init__(self, ureg):
        self.ureg = ureg


class PPLN(Crystal):
    def __init__(self, ureg):
        super().__init__(ureg)
        self.coeffs = {
            "e": {
                "a1": 5.756,
                "a2": 0.0983,
                "a3": 0.2020,
                "a4": 189.32,
                "a5": 12.52,
                "a6": 1.32e-2,
                "b1": 2.86e-6,
                "b2": 4.7e-8,
                "b3": 6.113e-8,
                "b4": 1.516e-4
            },
            "o": {
                "a1": 5.653,
                "a2": 0.1185,
                "a3": 0.2091,
                "a4": 89.61,
                "a5": 10.85,
                "a6": 1.97e-2,
                "b1": 7.941e-7,
                "b2": 3.134e-8,
                "b3": -4.641e-9,
                "b4": -2.188e-6
            },
        }

    @staticmethod
    def _get_temp_parameter(temp_celsius):
        return (temp_celsius - 24.5) * (temp_celsius + 570.82)

    # f is the temperature parameter
    @staticmethod
    def _get_refractive_index(wvl_um, f, c):
        return np.sqrt(c['a1'] + c['b1'] * f
                       + (c['a2'] + c['b2'] * f)/(wvl_um ** 2 - (c['a3'] + c['b3'] * f) ** 2)
                       + (c['a4'] + c['b4'] * f)/(wvl_um ** 2 - c['a5'] ** 2)
                       - c['a6'] * wvl_um ** 2)

    def get_refractive_index(self, axis, wavelength, temperature):
        temp_celsius = temperature.to(self.ureg.degC).magnitude
        wvl_um = wavelength.to(self.ureg.micrometer).magnitude
        temp_parameter = self._get_temp_parameter(temp_celsius)
        return self._get_refractive_index(wvl_um, temp_parameter, self.coeffs[axis])
