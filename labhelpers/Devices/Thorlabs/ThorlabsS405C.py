from .private.ThorlabsPowerSensor import _ThorlabsPowerSensor


class ThorlabsS310C(_ThorlabsPowerSensor):
    def __init__(self, ureg):
        linearity_err = 0.5/100
        calibration_err = {190: 5/100, 1063: 3/100, 1065: 5/100}
        wvl_range = (190 * ureg.nanometer, 20 * ureg.micrometer)
        super().__init__(linearity_err, calibration_err, wvl_range, ureg)
