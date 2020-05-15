import numpy as np
import matplotlib.pyplot as plt


def plot(infile, name_x, name_y, y_filter_func=None, label_x=None, label_y=None, genfromtxt_args=None, plot_args=None):
    x, y = _file_to_arrs(infile, name_x, name_y, y_filter_func, genfromtxt_args)

    if label_x is None:
        label_x = name_x
    if label_y is None:
        label_y = name_y

    return _create_fig(x, y, label_x, label_y, plot_args)


def _file_to_arrs(infile, name_x, name_y, y_filter_func, genfromtxt_args):
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


def _create_fig(x, y, label_x, label_y, plot_args):
    plot_args_default = {'color': 'blue',
                         'marker': '.',
                         'ls': ''}
    if plot_args is not None:
        plot_args_default.update(plot_args)

    fig, ax = plt.subplots()

    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.grid()
    ax.plot(x, y, **plot_args_default)
    return fig, ax
