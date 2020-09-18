from .private.ThorlabsPowerSensor import _ThorlabsPowerSensor


class ThorlabsS120VC(_ThorlabsPowerSensor):
    def __init__(self, ureg):
        linearity_err = 0.5/100
        calibration_err = {200: 7/100, 280: 5/100, 440: 3/100, 981: 7/100}
        wvl_range = (200 * ureg.nanometer, 1100 * ureg.nanometer)
        super().__init__(linearity_err, calibration_err, wvl_range, ureg)
