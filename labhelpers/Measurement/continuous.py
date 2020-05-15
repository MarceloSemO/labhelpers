import time
import numpy as np


def measure(timestep_s, meas_time_s, record_functions, headers, countdown_s=0, outfile=None):
    f = _init_file(outfile, headers)
    if countdown_s > 0:
        _start_countdown(countdown_s)
    start_s = time.time()
    print('Measurement started')
    if outfile is None:
        _print_headers_console(headers)
    time_elapsed_s = 0
    while time_elapsed_s < meas_time_s:
        start_single_meas_ns = time.time_ns()
        values = _do_measurement(time_elapsed_s, record_functions)
        _print_values(values, f)
        single_meas_time_s = (time.time_ns() - start_single_meas_ns) * 1e-9
        time.sleep(timestep_s - single_meas_time_s)
        time_elapsed_s = time.time() - start_s
    print('Measurement finished')
    if f is not None:
        f.close()


# TODO: replace with general funciton from utils
def _init_file(outfile, headers):
    if outfile is None:
        return None
    f = open(outfile, 'w+', buffering=1)
    f.write("Time (s), {}\n".format(', '.join(headers)))
    return f


def _start_countdown(countdown_s):
    for i in range(countdown_s, 0, -1):
        print('Starting measurement in {:d} seconds.'.format(i))
        time.sleep(1)
    return


def _print_headers_console(headers):
    outstr = "Time (s), {}".format(', '.join(headers))
    print("Time (s), {}".format(', '.join(headers)))
    print('-' * len(outstr))


def _do_measurement(time_elapsed_s, record_functions):
    meas_vals = np.array([time_elapsed_s])
    for rec_func in record_functions:
        meas_vals = np.append(meas_vals, rec_func())
    return meas_vals


def _print_values(values, f):
    outstr = np.array2string(values, formatter={'float_kind':lambda x: "%.5e" % x}, separator=', ')[1:-1]
    if f is None:
        print(outstr)
    else:
        f.write('{}\n'.format(outstr))


