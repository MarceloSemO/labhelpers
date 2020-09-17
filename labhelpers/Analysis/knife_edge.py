import numpy as np
import matplotlib.pyplot as plt
from lmfit import Model

from labhelpers.Analysis.functions import gauss_int
from labhelpers.Analysis.functions import beam_radius
from labhelpers.Analysis.data_management import file_to_arrs
from labhelpers.Utils.display import get_result_string
from labhelpers.Analysis.plot import create_fig


# evaluate data of knife edge measurement
def evaluate(infile, pos_err_func, pow_err_func, outfile='', reverse=True):
    # acquire data
    pos_mm, pow_W = file_to_arrs(infile, ['Position_mm', 'Power_W'])

    pos_err_mm = pos_err_func(pos_mm)
    pow_err_W = pow_err_func(pow_W)

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

    return result.best_values['w'], result.params['w'].stderr


def fit_z_profile(pos_mm, w_mm, w_err_mm, wvl_um, m=None):
    # set up model
    beam_model = Model(beam_radius, independent_vars=['z_mm'])
    params = beam_model.make_params(z0_mm=0,
                                    w0_mm=min(w_mm)/100,
                                    wvl_um=wvl_um,
                                    m=1
                                    )
    params['wvl_um'].set(vary=False)

    if m is None:
        # (Rayleigh range and waist independent)
        params['m'].set(min=1)
    else:
        # (Rayleigh range calculated from waist, assuming M = 1)
        params['m'].set(vary=False)
    result = beam_model.fit(w_mm, params, z_mm=pos_mm, weights=1/w_err_mm, scale_covar=False)
    print(result.fit_report())
    return result


def _fit(pos_mm, pow_W, pow_err_W, reverse):
    # set up model
    gauss_int_model = Model(gauss_int)
    params = gauss_int_model.make_params(max_val=max(pow_W) * 0.8,
                                         min_val=min(pow_W),
                                         x0=(max(pos_mm) + min(pos_mm)) / 2,
                                         w=(max(pos_mm) - min(pos_mm)) / 100,
                                         reverse=reverse)
    params['w'].set(min=0)
    params['reverse'].set(vary=False)
    #params['max_val'].set(vary=False)
    #params['min_val'].set(vary=False)
    # fit function to data
    result = gauss_int_model.fit(pow_W, params, x=pos_mm, weights=1 / pow_err_W, scale_covar=False)
    print(result.fit_report())
    return result
