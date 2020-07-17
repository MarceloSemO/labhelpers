import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from labhelpers.Analysis.functions import gauss2d_flat


def str_to_img(im_str):
    return plt.imread(im_str)[:, :, 0]


def make_grid(img):
    x = np.linspace(0, img.shape[1]-1, img.shape[1])
    y = np.linspace(0, img.shape[0]-1, img.shape[0])
    return np.meshgrid(x, y)


def find_max_pos(img):
    return np.unravel_index(img.argmax(), img.shape)


# guess width of Gaussian distribution along given axis
def guess_sigma(img, axis, max_pos=None):
    if max_pos is None:
        max_pos = find_max_pos(img)
    if axis == "x":
        # max_pos[0] is y-coordinate of maximum
        gauss1d = img[max_pos[0], :]
        return np.abs(max_pos[1] - np.abs(gauss1d - gauss1d.max() * 0.135).argmin())
    elif axis == "y":
        # max_pos[1] is x-coordinate of maximum
        gauss1d = img[:, max_pos[1]]
        return np.abs(max_pos[0] - np.abs(gauss1d - gauss1d.max() * 0.135).argmin())
    else:
        raise ValueError("Axis must be either 'x' or 'y'.")


def create_figure(img_scaled, popt):
    gridsize = 4

    (x0, y0, sigma_x, sigma_y) = popt[:4]
    fig = plt.figure()
    ax_2d = plt.subplot2grid((gridsize, gridsize), (0, 1), rowspan=gridsize - 1, colspan=gridsize - 1)
    ax_v = plt.subplot2grid((gridsize, gridsize), (0, 0), rowspan=gridsize - 1, colspan=1)
    ax_h = plt.subplot2grid((gridsize, gridsize), (gridsize - 1, 1), rowspan=1, colspan=gridsize - 1)
    ax_2d.imshow(img_scaled)
    ax_2d.set_xlabel('Horizontal pixel number')
    ax_2d.set_ylabel('Vertical pixel number')

    phi = np.linspace(0, 2 * np.pi)
    x = x0 + sigma_x * np.cos(phi)
    y = y0 + sigma_y * np.sin(phi)
    ax_2d.plot(x, y)

    ax_2d.axvline(x0, c='red')
    ax_2d.axhline(y0, c='red')
    img_size_y = np.size(img_scaled[:, 0])
    ax_v.invert_yaxis()
    ax_v.set_xlim(0, 1)
    ax_v.plot(img_scaled[:, int(round(x0))], np.linspace(0, img_size_y - 1, num=img_size_y))
    ax_h.plot(img_scaled[int(round(y0)), :])
    return fig


# fit 2D Gaussian to Greyscale png
# 'img' must be a matrix or a string specifying the filename
def fit_gauss_2d(img, plot=True):
    if type(img) == str:
        img = str_to_img(img)
    xy_mesh = make_grid(img)
    # initial guess: use maximum
    max_pos = find_max_pos(img)
    p0 = (max_pos[1], max_pos[0], guess_sigma(img, "x", max_pos), guess_sigma(img, "y", max_pos), 1, 0)
    img_scaled = img/img.max()
    popt, pcov = opt.curve_fit(gauss2d_flat, xy_mesh, img_scaled.ravel(), p0=p0)
    if not plot:
        return popt
    return popt, create_figure(img_scaled, popt)
