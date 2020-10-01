import numpy as np
from labhelpers.Simulation.Crystal import *
from labhelpers.Simulation.RefractiveIndex import RefractiveIndex as RefInd


class QPM:
    def __init__(self, ureg):
        self.ureg = ureg

    # wvls and ref_ind are numpy arrays of length 3 [input1, input2, output]
    def qpm_period(self, wvls, ref_inds):
        addends = ref_inds / wvls
        return (1/(addends[2] - addends[1] - addends[0])).to(self.ureg.micrometer)

    @staticmethod
    def qpm_mismatch(wvls, ref_inds, grating_period):
        k = 2 * np.pi * ref_inds / wvls
        return k[2] - (k[0] + k[1] + 2 * np.pi / grating_period)


    def qpm_mismatch_2(self, material, source, axis, wvl_in_1_um, wvl_in_2_um, tmp_celsius, grating_period,
                     interaction='sum', qpm_order=1):
        ref_ind = RefInd()
        if interaction == 'sum':
            wvl_out_um = 1 / (1 / wvl_in_1_um + 1 / wvl_in_2_um)
        elif interaction == 'diff':
            wvl_out_um = 1 / abs(1 / wvl_in_1_um - 1 / wvl_in_2_um)
        else:
            raise (ValueError, "Interaction must be 'sum' or 'diff'. ")
        n_in_1 = ref_ind.refractive_index(material, source, axis, wvl_in_1_um, tmp_celsius)
        n_in_2 = ref_ind.refractive_index(material, source, axis, wvl_in_2_um, tmp_celsius)
        n_out = ref_ind.refractive_index(material, source, axis, wvl_out_um, tmp_celsius)
        k_in_1 = 2 * np.pi * n_in_1 / wvl_in_1_um
        k_in_2 = 2 * np.pi * n_in_2 / wvl_in_2_um
        k_out = 2 * np.pi * n_out / wvl_out_um
        return k_out - k_in_1 - k_in_2 - 2 * np.pi * qpm_order / grating_period

    def conv_eff(self, material, source, axis, wvl_in_1_um, wvl_in_2_um,
                 tmp_celsius, grating_period, interaction='sum', qpm_order=1):
        dk_qpm = self.qpm_mismatch_2(material,
                                   source,
                                   axis,
                                   wvl_in_1_um,
                                   wvl_in_2_um,
                                   tmp_celsius,
                                   grating_period,
                                   interaction=interaction,
                                   qpm_order=qpm_order)
        return (np.sin(dk_qpm * 5000/ 2)) ** 2 / (dk_qpm * 5000 / 2) ** 2
