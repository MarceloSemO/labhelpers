import math
import numpy as np
from labhelpers.Analysis.functions import sign


# get string for measurement result including error
def get_result_string(value, error, latex=True):
    err_pos = _get_first_digit_pos(error)
    val_pos = _get_first_digit_pos(value)
    sign_digits = val_pos - err_pos + 1
    val = _round_tie_away_from_zero(value, -(val_pos - sign_digits + 1))
    err = _round_meas_err(error)
    if latex:
        return "(" + str(val) + r" $\pm$ " + str(err) + ")"
    else:
        return "(" + str(val) + " +/- " + str(err) + ")"


# get position of first significant digit
def _get_first_digit_pos(x):
    return int(math.floor(math.log10(abs(x))))


# get digit of number x at position pos
def _get_digit_at(x, pos):
    return int(abs(x * 10 ** (-pos)) % 10)


# round measurement errors correctly
def _round_meas_err(err):
    decimal = - _get_first_digit_pos(err)
    if err < 0:
        return math.floor(err * 10 ** decimal) / (10 ** decimal)
    else:
        return math.ceil(err * 10 ** decimal) / (10 ** decimal)


def _round_tie_away_from_zero(val, decimal):
    last_digit = _get_digit_at(val, -(decimal + 1))
    if last_digit == 5:
        return round(val + sign(val) * 10 ** -(decimal+1), decimal)
    else:
        return round(val, decimal)
