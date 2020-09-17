import numpy as np
import pint


class Measurement:

    def measure(self, func):
        return self.measure_n(1, func)

    @staticmethod
    def measure(self, func):
        return self.measure_n(1, func)

    @staticmethod
    def measure_n(n: int, func):
        if type(n) != int:
            raise TypeError("Number of measurements must be integer value.")
        if n < 1:
            raise ValueError("Number of measurements must be 1 or larger.")
        if n == 1:
            result = func()
            try:
                return np.array([result])
            except ValueError:
                return np.array([result.magnitude]) * result.units
        else:
            vals = np.zeros(n)
            result = func()
            try:
                vals[0] = result
                for i in range(1, n):
                    vals[i] = func()
            except ValueError:
                vals[0] = result.magnitude
                unit = result.units
                for i in range(n):
                    vals[i] = func().magnitude
                vals = vals * unit
            return vals.mean(), vals.std(ddof=1)
