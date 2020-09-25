import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os.path
from typing import Union, List

from labhelpers.Analysis.data_management import file_to_arrs

def configure_matplotlib():
    if not matplotlib.rcParams['text.usetex']:
        matplotlib.rcParams['text.usetex'] = True
        f = open(os.path.join(os.path.dirname(__file__), 'defaults.json'))
        matplotlib.rcParams.update(json.load(f)["matplotlib_params"])
        matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}']
        f.close()


def plot_from_file(infile, name_x: str, name_y: Union[str, List[str]],
                   y_filter_func=None, label_x=None, label_y=None,
                   genfromtxt_args=None, plot_args=None):
    if type(name_y) == list:
        names = [name_x, *name_y]
        _, (x, *y) = file_to_arrs(infile, names, y_filter_func, genfromtxt_args)
    else:
        names = [name_x, name_y]
        _, (x, y) = file_to_arrs(infile, names, y_filter_func, genfromtxt_args)


    if label_x is None:
        label_x = name_x
    if label_y is None:
        if type(name_y) == str:
            label_y = name_y
        else: label_y = ""

    return create_fig(x, y, label_x, label_y, plot_args=plot_args)


def open_defaults():
    f = open(os.path.join(os.path.dirname(__file__), 'defaults.json'))
    defaults = json.load(f)
    f.close()
    return defaults


def create_fig(x, y, label_x, label_y, xerr=None, yerr=None, plot_args=None):
    configure_matplotlib()
    defaults = open_defaults()
    if callable(y):
        plot_args_default = defaults['plot_args_line']
    else:
        plot_args_default = defaults['plot_args_errorbar']

    fig, ax = plt.subplots()

    ax.set_xlabel(label_x)
    ax.set_ylabel(label_y)
    ax.grid()
    if plot_args is not None:
        plot_args_default.update(plot_args)

    if callable(y):
        plot_args_default['color'] = plot_args_default['color'][0]
        ax.plot(x, y(x), **plot_args_default)
    elif type(y) == list:
        if yerr is None:
            yerr = [None] * len(y)
            _plot_args_default = plot_args_default.copy()
        for i in range(len(y)):
            _plot_args_default['color'] = plot_args_default['color'][i]
            for key in plot_args.keys():
                if type(plot_args_default[key]) == list:
                    _plot_args_default[key] = plot_args_default[key][i]
            ax.errorbar(x, y[i], xerr=xerr, yerr=yerr[i], **_plot_args_default)
    else:
        plot_args_default['color'] = plot_args_default['color'][0]
        ax.errorbar(x, y, xerr=xerr, yerr=yerr, **plot_args_default)
    return fig, ax


def create_colormap(*args):
    if len(args) == 2:
        (z, label_z) = args
    elif len(args) == 6:
        (x, y, z, label_x, label_y, label_z) = args
    else:
        raise (TypeError, f'create_colormap() takes 2 or 6 arguments. {len(args)} arguments were given')


# by Scott Zentoni
def multiple_formatter(denominator=2, number=np.pi, counter_str='\pi', den_str=None):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def _multiple_formatter(x, pos):
        den = denominator
        num = np.int(np.rint(den * x / number))
        com = gcd(num, den)
        (num, den) = (int(num / com), int(den / com))
        if den == 1:
            if num == 0:
                result = r'$0$'
            elif num == 1:
                result = r'$%s$' % counter_str
            elif num == -1:
                result = r'$-%s$' % counter_str
            else:
                result = r'$%s%s$' % (num, counter_str)
        else:
            if num == 1:
                result = r'$\frac{%s}{%s}$' % (counter_str, den)
            elif num == -1:
                result = r'$\frac{-%s}{%s}$' % (counter_str, den)
            else:
                result = r'$\frac{%s%s}{%s}$' % (num, counter_str, den)
        if den_str is None or num == 0:
            return result
        else:
            if den == 1:
                return result[:1] + r'\frac{' + result[1:-1] + r'}{%s}' % den_str + result[-1:]
            else:
                return result[:-2] + r' %s' % den_str + result[-2:]

    return _multiple_formatter
