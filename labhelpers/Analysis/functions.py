import numpy as np
from scipy.special import erf
import pint

ureg = pint.UnitRegistry()


# calculates the integrated Gaussian distribution
def gauss_int(x, max_val, min_val, x0, w, reverse):
    if not reverse:
        return (max_val - min_val) / 2 * (1 + erf(np.sqrt(2) * (x - x0) / w)) + min_val
    else:
        return (max_val - min_val) / 2 * (1 - erf(np.sqrt(2) * (x - x0) / w)) + min_val


# calculates 2-dimensional Gaussian
def gauss2d(xy, x0, y0, sigma_x, sigma_y, amp, offset):
    (x, y) = xy
    #x, y = np.meshgrid(x, y)
    return amp * np.exp(- 2 * ((x-x0) ** 2 / (sigma_x ** 2) + (y-y0) ** 2 / sigma_y ** 2)) + offset


# calculates 2-dimensional Gaussian and returns a flattened array
def gauss2d_flat(xy, x0, y0, sigma_x, sigma_y, amp, offset):
    return gauss2d(xy, x0, y0, sigma_x, sigma_y, amp, offset).ravel()


# signum function
def sign(x):
    return 1 if x >= 0 else -1


# linear function
def lin(x, m, n):
    return m * x + n


# sinc^2 function
def sinc2(x, x0, a, b, y0):
    return a * (np.sinc(b / np.pi * (x-x0))) ** 2 + y0


# calcualte beam radius of Gaussian beam
def beam_radius(z_mm, w0_mm, z0_mm, wvl_um, m):
    zr = np.pi * w0_mm ** 2 / (m ** 2 * wvl_um * 1e-3)
    return w0_mm * np.sqrt(1 + (z_mm - z0_mm) ** 2 / zr ** 2)


def sin2_root(x, x0, a, b, y0):
    return a * (np.sin(b * np.sqrt(x-x0))) ** 2 + y0

# calculate temperature for given resistance of NTC thermistor (B-parameter equation)
def b_param_eq(r, t_0, r_0, b, temp_unit='celsius'):
    if hasattr(t_0, 'magnitude'):
        return 1 / ((1 / t_0.to(ureg.kelvin)) + 1/b * np.log(r/r_0))
    else:
        if temp_unit == 'celsius':
            return 1 / ((1 / (t_0 + 273.15)) + 1/b * np.log(r/r_0)) - 273.15
        elif temp_unit == 'kelvin':
            return 1 / ((1 / t_0) + 1 / b * np.log(r / r_0))
        else:
            raise ValueError("Parameter temp_unit must be either 'celsius' or 'kelvin'.")


def b_param_eq_err(r, t_0, r_0, b, r_err=0, t_0_err=0, r_0_err=0, b_err=0, err_in='rel', temp_unit='celsius'):
    t = b_param_eq(r, t_0, r_0, b, temp_unit)
    # change quantities to Kelvin, if necessary
    if hasattr(t_0, 'magnitude'):
        t = t.to(ureg.kelvin)
        t_0 = t_0.to(ureg.kelvin)
    elif temp_unit == 'celsius':
        t += 273.15
        t_0 += 273.15
    # calculate relative errors, if absolute errors are given
    if err_in == 'abs':
        r_err /= r
        t_0_err /= t_0
        r_0_err /= r_0
        b_err /= b
    elif err_in != 'rel':
        raise ValueError("Parameter err_in must be either 'rel' or 'abs'.")
    # calculate temperature error
    return t * np.sqrt((t/t_0 * t_0_err) ** 2 + ((t-t_0)/t_0 * b_err) ** 2 + (t/b * r_0_err) ** 2 + (t/b * r_err) ** 2)


def tanh2_root(x, a, b, x0, y0):
    return (a-y0) * np.tanh(b * np.sqrt(x-x0)) + y0
