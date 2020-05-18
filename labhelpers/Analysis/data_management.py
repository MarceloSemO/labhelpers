import numpy as np


def file_to_arrs(infile, name_x, name_y, y_filter_func=None, genfromtxt_args=None):
    genfromtxt_args_default = {'delimiter': ',',
                               'names': True}
    if genfromtxt_args is not None:
        genfromtxt_args_default.update(genfromtxt_args)

    f = open(infile, 'r')
    data = np.genfromtxt(f, **genfromtxt_args_default)
    f.close()
    x, y = _data_to_arrs(data, name_x, name_y)
    return _filter_data(x, y, y_filter_func)


def _data_to_arrs(data, name_x, name_y):
    try:
        x = data[name_x]
        y = data[name_y]
        return x, y
    except ValueError as err:
        print('Existing fields names are:', data.dtype.names)
        raise err


def _filter_data(x, y, y_filter_func):
    if y_filter_func is None:
        return x, y
    y_filter = y_filter_func(y)
    return x[y_filter], y[y_filter]
