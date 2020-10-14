import numpy as np


class Crystal:
    def __init__(self, ureg):
        self.ureg = ureg


class PPLN(Crystal):
    def __init__(self, ureg):
        super().__init__(ureg)
        # source: Gayer et al., Appl. Phys B, 91, 343-348 (2008)
        self.data = {
            "Gayer2008": {
                "coeffs": {
                    # 5% MgO doped CLN
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
                    }
                },
                "ranges": {
                    "wavelength": (0.5, 4) * ureg.micrometer,
                    "temperature": (ureg.Quantity(21, ureg.degC), ureg.Quantity(200, ureg.degC))
                }
            },
            "Zelmon1997": {
                "coeffs": {
                    "o": {
                        'a': 2.4272,
                        'b': 0.01478,
                        'c': 1.4617,
                        'd': 0.05612,
                        'e': 9.6536,
                        'f': 371.216

                    },
                    "e": {
                        'a': 2.2454,
                        'b': 0.01242,
                        'c': 1.3005,
                        'd': 0.05313,
                        'e': 6.8972,
                        'f': 331.33
                    }
                },
                "ranges": {
                    "wavelength": (0.5, 5) * ureg.micrometer
                }
            }
        }


    @staticmethod
    def _get_temp_parameter(temp_celsius):
        return (temp_celsius - 24.5) * (temp_celsius + 570.82)

    # f is the temperature parameter
    @staticmethod
    def _get_refractive_index_gayer(wvl_um, f, c):
        return np.sqrt(c['a1'] + c['b1'] * f
                       + (c['a2'] + c['b2'] * f)/(wvl_um ** 2 - (c['a3'] + c['b3'] * f) ** 2)
                       + (c['a4'] + c['b4'] * f)/(wvl_um ** 2 - c['a5'] ** 2)
                       - c['a6'] * wvl_um ** 2)

    @staticmethod
    def _get_refractive_index_zelmon(wvl_um, c):
        return np.sqrt(1 + c['a'] * wvl_um ** 2 / (wvl_um ** 2 - c['b'])
                       + c['c'] * wvl_um ** 2 / (wvl_um ** 2 - c['d'])
                       + c['e'] * wvl_um ** 2 / (wvl_um ** 2 - c['f']))

    def get_refractive_index(self, source, axis, wavelength, temperature=None):
        wvl_range = self.data[source]["ranges"]["wavelength"]
        if wavelength < wvl_range[0] or wavelength > wvl_range[1]:
            raise ValueError('Wavelength out of range.')
        wvl_um = wavelength.to(self.ureg.micrometer).magnitude
        if source == "Gayer2008":
            temp_range = self.data[source]["ranges"]["temperature"]
            if temperature is None:
                raise ValueError('Temperature must not be None for this source.')
            elif temperature < temp_range[0] or temperature > temp_range[1]:
                raise ValueError('Temperature out of range.')
            else:
                temp_celsius = temperature.to(self.ureg.degC).magnitude
                temp_parameter = self._get_temp_parameter(temp_celsius)
                return self._get_refractive_index_gayer(wvl_um, temp_parameter, self.data[source]["coeffs"][axis])
        else:
            return self._get_refractive_index_zelmon(wvl_um, self.data[source]["coeffs"][axis])
