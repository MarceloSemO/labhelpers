import time
import numpy as np


def measure(timestep_s, meas_time_s, record_functions, headers, countdown_s=0, add_timestamp=False, outfile=None):
    """
    Start a continuous measurement.
    :param timestep_s: Time interval (in seconds) between two measurements.
    :param meas_time_s: Total time (in seconds) to run measurement.
    :param record_functions: Functions to execute at each measurement point.
        Each one must return one single measurement value.
    :param headers: Labels of the measured quantities.
    :param countdown_s: Time (in seconds) to wait until start of measurement (Default: 0).
    :param add_timestamp: True if a timestamp with the current time should be added to the beginning of the output
        (Default: False).
    :param outfile: File to save measurement to. If None (default), the results are written to the console.
    :return: None
    """
    f = _init_file(outfile, headers, add_timestamp)
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
        if single_meas_time_s < timestep_s:
            time.sleep(timestep_s - single_meas_time_s)
        time_elapsed_s = time.time() - start_s
    print('Measurement finished')
    if f is not None:
        f.close()


# TODO: replace with general funciton from utils
def _init_file(outfile, headers, add_timestamp):
    if outfile is None:
        return None
    f = open(outfile, 'w+', buffering=1)
    if add_timestamp:
        f.write(time.asctime() + "\n")
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


