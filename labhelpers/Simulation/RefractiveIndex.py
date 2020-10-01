import numpy as np

"""
Returns the refractive index of
 - a given material
 - using the Sellmeier equation in the given source
 - for a given axis
 - for a given wavelength
 - for a given temperature
"""


class RefractiveIndex:

    def __init__(self):
        self.ref_ind = {
            "ktp": {
                # J. Opt. Soc. Am. B, 6, 622-633 (1989)
                "Bierlein, Vanherzeele": {
                    "n": {
                        "x": {
                            "a": 2.1146,
                            "b": 0.89188,
                            "c": 0.20861,
                            "d": 0.01320
                        },
                        "y": {
                            "a": 2.1518,
                            "b": 0.87862,
                            "c": 0.21801,
                            "d": 0.01327
                        },
                        "z": {
                            "a": 2.3136,
                            "b": 1.00012,
                            "c": 0.23831,
                            "d": 0.01679
                        },
                        "function": lambda axis, wvl_um, tmp_celsius, a, b, c, d:
                        np.sqrt(a + b / (1 - (c / wvl_um) ** 2) - d * wvl_um)
                    }
                },
                # Appl. Opt., 41, 5040-5044 (2002)
                "Kato, Takaoka": {
                    "n": {
                        "x": {
                            "a0": 3.291,
                            "a1": 0.0414,
                            "a2": 9.35522,
                            "b1": 0.03978,
                            "b2": 31.45571
                        },
                        "y": {
                            "a0": 3.45018,
                            "a1": 0.04341,
                            "a2": 16.98825,
                            "b1": 0.04597,
                            "b2": 39.43799
                        },
                        "z": {
                            "a0": 4.59423,
                            "a1": 0.06206,
                            "a2": 110.80672,
                            "b1": 0.04763,
                            "b2": 86.12171
                        },
                        "function": lambda axis, wvl_um, tmp_celsius, a0, a1, a2, b1, b2:
                        np.sqrt(a0 + a1 / (wvl_um ** 2 - b1) + a2 / (wvl_um ** 2 - b2))
                        + self.ref_ind['ktp']['Kato, Takaoka']['dn_dT']["function"]
                        (wvl_um, **(self.ref_ind['ktp']['Kato, Takaoka']['dn_dT'][axis])) * (tmp_celsius - 20.0)
                    },
                    "dn_dT": {
                        "x": {
                            "c0": 0.1627,
                            "c1": 0.8416,
                            "c2": -0.5353,
                            "c3": 0.1717
                        },
                        "y": {
                            "c0": 0.5425,
                            "c1": 0.5154,
                            "c2": -0.4063,
                            "c3": 0.1997
                        },
                        "z": {
                            "c0": -0.1897,
                            "c1": 3.6677,
                            "c2": -2.9220,
                            "c3": 0.9221
                        },
                        "function": lambda wvl_um, c0, c1, c2, c3:
                        (c0 + c1 / wvl_um + c2 / wvl_um ** 2 + c3 / wvl_um ** 3) * 1e-5
                    }
                }
            }

        }

    def refractive_index(self, material, source, axis, wvl_um, tmp_celsius=20.0):
        coeffs_n = self.ref_ind[material][source]["n"][axis]
        return self.ref_ind[material][source]["n"]["function"](axis, wvl_um, tmp_celsius, **coeffs_n)
