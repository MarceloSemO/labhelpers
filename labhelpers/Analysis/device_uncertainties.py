# collection of functions to calculate measurement error of measurement from specific device
import pint


class DeviceUncertainties:
    def __init__(self):
        self.ureg = pint.UnitRegistry()

    def thorlabs_s120vc_err(self, power, err_type, wvl=None):
        if err_type.lower() == 'linearity':
            return 0.5 / 100 * power
        if err_type.lower() == 'calibration':
            if wvl is None:
                raise ValueError('Wavelength must not be None for calibration error.')
            else:
                if wvl < 200 * self.ureg.nanometer:
                    raise ValueError("Wavelength too short. Minimum wavelength is 200 nm.")
                elif wvl <= 279 * self.ureg.nanometer:
                    return 7 / 100 * power
                elif wvl <= 439 * self.ureg.nanometer:
                    return 5 / 100 * power
                elif wvl <= 980 * self.ureg.nanometer:
                    return 3 / 100 * power
                elif wvl <= 1100 * self.ureg.nanometer:
                    return 7 / 100 * power
                else:
                    raise ValueError("Wavelength too long. Maximum wavelength is 1100 nm.")

    def thorlabs_s405c_err(self, power, err_type, wvl=None):
        if err_type.lower() == 'linearity':
            return 0.5 / 100 * power
        if err_type.lower() == 'calibration':
            if wvl is None:
                raise ValueError('Wavelength must not be None for calibration error.')
            else:
                if wvl < 190 * self.ureg.nanometer or wvl > 20 * self.ureg.micrometer:
                    raise ValueError("Wavelength out of range (0.19 - 20 µm)")
                elif wvl == 1064:
                    return 3 / 100 * power
                else:
                    return 5 / 100 * power
