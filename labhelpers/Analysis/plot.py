import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import json
import os.path

from labhelpers.Analysis.data_management import file_to_arrs

def configure_matplotlib():
    if not matplotlib.rcParams['text.usetex']:
        matplotlib.rcParams['text.usetex'] = True
        f = open(os.path.join(os.path.dirname(__file__), 'defaults.json'))
        matplotlib.rcParams.update(json.load(f)["matplotlib_params"])
        matplotlib.rcParams['text.latex.preamble'] = [r'\usepackage[cm]{sfmath}']
        f.close()


def plot_from_file(infile, name_x, name_y, y_filter_func=None, label_x=None, label_y=None, genfromtxt_args=None,
                   plot_args=None):
    x, y = file_to_arrs(infile, [name_x, name_y], y_filter_func, genfromtxt_args)

    if label_x is None:
        label_x = name_x
    if label_y is None:
        label_y = name_y

    return create_fig(x, y, label_x, label_y, plot_args)


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
    if callable(y):
        if plot_args is not None:
            plot_args_default.update(plot_args)
        ax.plot(x, y(x), **plot_args_default)
    else:
        if plot_args is not None:
            plot_args_default.update(plot_args)
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
def multiple_formatter(denominator=2, number=np.pi, latex='\pi'):
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
                return r'$0$'
            if num == 1:
                return r'$%s$' % latex
            elif num == -1:
                return r'$-%s$' % latex
            else:
                return r'$%s%s$' % (num, latex)
        else:
            if num == 1:
                return r'$\frac{%s}{%s}$' % (latex, den)
            elif num == -1:
                return r'$\frac{-%s}{%s}$' % (latex, den)
            else:
                return r'$\frac{%s%s}{%s}$' % (num, latex, den)

    return _multiple_formatter
