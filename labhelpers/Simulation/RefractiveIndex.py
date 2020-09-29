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
            "ppln_c_05mgo": {
                # Appl. Phys B, 91, 343-348 (2008)
                "Gayer, Sacks, Galun, Arie": {
                    "n": {
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
                        "function": lambda axis, wvl_um, temp_celsius, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4:
                        np.sqrt(a1
                                + b1 * self.ref_ind['ppln_c_05mgo']['Gayer, Sacks, Galun, Arie']['n'][axis][temp_celsius]),
                        "_function": 2,
                    }
                }
            },
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
