import matplotlib.pyplot as plt
from labhelpers.Analysis.data_management import file_to_arrs


def plot_from_file(infile, name_x, name_y, y_filter_func=None, label_x=None, label_y=None, genfromtxt_args=None, plot_args=None):
    x, y = file_to_arrs(infile, [name_x, name_y], y_filter_func, genfromtxt_args)

    if label_x is None:
        label_x = name_x
    if label_y is None:
        label_y = name_y

    return create_fig(x, y, label_x, label_y, plot_args)


def create_fig(x, y, label_x, label_y, xerr=None, yerr=None, plot_args=None):
    plot_args_default = {'color': 'blue',
                         'marker': '+',
                         'ls': ''}
    if plot_args is not None:
        plot_args_default.update(plot_args)

    fig, ax = plt.subplots()

    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.grid()
    ax.errorbar(x, y, xerr=xerr, yerr=yerr, **plot_args_default)
    return fig, ax
