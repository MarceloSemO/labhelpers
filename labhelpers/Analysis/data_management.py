import numpy as np
import time


def file_to_arrs(infile, names, y_filter_func=None, genfromtxt_args=None):
    genfromtxt_args_default = {'delimiter': ',',
                               'names': True}
    if genfromtxt_args is not None:
        genfromtxt_args_default.update(genfromtxt_args)

    f = open(infile, 'r')
    header = _get_header(f)
    data = np.genfromtxt(f, **genfromtxt_args_default)
    f.close()
    if len(names) == 2:
        x, y = _data_to_arrs(data, names)
        return header, _filter_data(x, y, y_filter_func)
    else:
        return header, _data_to_arrs(data, names)


def _get_header(file):
    header = {}
    for line in file:
        if line == "DATA:\n":
            _format_header(header)
            return header
        else:
            _update_header(header, line)


def _update_header(header, line):
    key, val = line.split(":", 1)
    # delete line separator character at end of value and leading whitespaces
    val = val[:-1].lstrip()
    if key in header:
        print(f"WARNING: Key {key} is already contained in header and will be overwritten.")
    header.update({key: val})


def _format_header(header):
    if 'TIME' in header:
        header['TIME'] = time.mktime(time.strptime(header['TIME']))


def _data_to_arrs(data, names):
    try:
        variables = []
        for name in names:
            variables.append(data[name])
        return variables
    except ValueError as err:
        print('Existing fields names are:', data.dtype.names)
        raise err


def _filter_data(x, y, y_filter_func):
    if y_filter_func is None:
        return x, y
    y_filter = y_filter_func(y)
    return x[y_filter], y[y_filter]
