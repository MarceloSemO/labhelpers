import numpy as np
import matplotlib.pyplot as plt


def plot(infile, name_x, name_y, y_filter_func=None, label_x=None, label_y=None, **kwargs):
    f = open(infile, 'r')
    data = np.genfromtxt(f, **kwargs)
    x, y = _data_to_arr(data, name_x, name_y)
    x, y = _filter_data(x, y, y_filter_func)
    if label_x is None:
        label_x = name_x
    if label_y is None:
        label_y = name_y
    return _create_fig(x, y, label_x, label_y)


def _data_to_arr(data, name_x, name_y):
    try:
        x = data[name_x]
        y = data[name_y]
        return x, y
    except ValueError as err:
        print('Existing fields names are:', data.dtype.names)
        raise err


def _filter_data(x, y, y_filter_func):
    y_filter = y_filter_func(y)
    return x[y_filter], y[y_filter]


def _create_fig(x, y, label_x, label_y):
    fig, ax = plt.subplots()

    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.grid()
    ax.plot(x, y, 'b.')
    return fig, ax
