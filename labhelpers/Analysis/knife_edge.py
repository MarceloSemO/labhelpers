import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model

from labhelpers.Analysis.functions import gauss_int
from labhelpers.Analysis.data_management import file_to_arrs
from labhelpers.Utils.display import get_result_string
from labhelpers.Analysis.plot import create_fig


# evaluate data of knife edge measurement
# TODO: also allow function for power and position error
def evaluate(infile, outfile='', pos_err_mm=0.005, reverse=True):
    # acquire data
    pos_mm, pow_W = file_to_arrs(infile, 'Position_mm', 'Power_W')
    pow_err_W = np.full_like(pow_W, 1e-4)

    # perform fit
    result = _fit(pos_mm, pow_W, pow_err_W, reverse)

    # plot figure
    fig, ax = create_fig(pos_mm, pow_W, "Position (mm)", "Power (W)", xerr=pos_err_mm, yerr=pow_err_W)
    ax.plot(pos_mm, result.best_fit, 'r--')

    # generate text box
    beam_radius_text = r"1/$e^2$ Beam radius $w$ = " \
                       + get_result_string(result.best_values['w'], result.params['w'].stderr) \
                       + " mm"
    chi2_text = r"$\chi^2_{ndf}$ = " + np.str(np.round(result.redchi, 2))
    result_text = '\n'.join((
        beam_radius_text,
        chi2_text))
    props = dict(boxstyle='round', facecolor='wheat', alpha=1)
    ax.text(min(pos_mm) + 0.1 * (max(pos_mm) - min(pos_mm)),
            min(pow_W) + 0.2 * (max(pow_W) - min(pow_W)),
            result_text, fontsize=6, bbox=props)

    if outfile == '':
        plt.savefig(''.join((infile.split(".")[:-1]) + ['.pdf']))
        plt.savefig(''.join((infile.split(".")[:-1]) + ['.svg']))
        plt.savefig(''.join((infile.split(".")[:-1]) + ['.png']))
    else:
        plt.savefig(outfile)
    plt.show()
    plt.close()


def _fit(pos_mm, pow_W, pow_err_W, reverse):
    # set up model
    gauss_int_model = Model(gauss_int)
    params = gauss_int_model.make_params(max_val=max(pow_W),
                                         min_val=min(pow_W),
                                         x0=(max(pos_mm) + min(pos_mm)) / 2,
                                         w=(max(pos_mm) + min(pos_mm)) / 4,
                                         reverse=reverse)
    params['w'].set(min=0)
    params['reverse'].set(vary=False)

    # fit function to data
    result = gauss_int_model.fit(pow_W, params, x=pos_mm, weights=1/pow_err_W, scale_covar=False)
    print(result.fit_report())
    return result
