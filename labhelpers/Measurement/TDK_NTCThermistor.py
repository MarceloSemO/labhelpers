from pathlib import Path
import numpy as np

from labhelpers.Analysis.data_management import file_to_arrs


class TDK_NTC:
    def __init__(self, char_no, r_25_kohm):
        self.char_no = char_no
        self.r_25_kohm = r_25_kohm
        path = Path(__file__).parent / "ntc_characteristics/{:d}.txt".format(char_no)
        self.temps_c, self.r_t_r_25, self.alpha = file_to_arrs(path, ["Temperature_DegC", "R_TR_25", "AlphaK"])

    def get_resistance(self, temp_celsius):
        idx = np.searchsorted(self.temps_c, temp_celsius)
        # calculate resistance at lower bound of temperature interval (see TDK standardized R/T characteristics)
        r_tx = self.r_25_kohm * self.r_t_r_25[idx]
        return r_tx * np.exp(self.alpha[idx]/100 * (self.temps_c[idx] + 273.15) ** 2 *
                             (1 / (temp_celsius + 273.15) - 1 /(self.temps_c[idx] + 273.15)))

    def get_temp(self, r_t_kohm):
        idx = -(np.searchsorted(np.sort(self.r_t_r_25), r_t_kohm / self.r_25_kohm) + 1)
        return (self.temps_c[idx] + 273.15) ** 2 / (np.log(r_t_kohm/(self.r_t_r_25[idx] * self.r_25_kohm)) *
                                                    100/self.alpha[idx] + self.temps_c[idx] + 273.15) - 273.15
