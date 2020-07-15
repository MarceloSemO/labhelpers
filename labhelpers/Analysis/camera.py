import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from labhelpers.Analysis.functions import gauss2d_flat


def str_to_img(im_str):
    return plt.imread(im_str)[:, :, 0]


def make_axes(img):
    x = np.linspace(0, img.shape[1]-1, img.shape[1])
    y = np.linspace(0, img.shape[0]-1, img.shape[0])
    return x, y


def find_max_pos(img):
    return np.unravel_index(img.argmax(), img.shape)


def guess_sigma(img, axis, max_pos=None):
    if max_pos is None:
        max_pos = find_max_pos(img)
    if axis == "x":
        max_pos = max_pos[0]
        gauss1d = img[max_pos, :]
    elif axis == "y":
        max_pos = max_pos[1]
        gauss1d = img[:, max_pos]
    else:
        raise ValueError("Axis must be either 'x' or 'y'.")
    max_val = gauss1d.max()
    return np.abs(max_pos - np.abs(gauss1d - max_val * 0.135).argmin())


# fit 2D Gaussian to Greyscale png
# 'img' must be a matrix or a string specifying the filename
def fit_gauss_2d(img):
    if type(img) == str:
        img = str_to_img(img)
    x_ax, y_ax = make_axes(img)
    # initial guess: use maximum
    max_pos = find_max_pos(img)
    p0 = (max_pos[0], max_pos[1], guess_sigma(img, "x", max_pos), guess_sigma(img, "y", max_pos), 1, 0)
    img_scaled = img/img.max()
    popt, pcov = opt.curve_fit(gauss2d_flat, (x_ax, y_ax), img_scaled.ravel(), p0=p0)
    return popt
