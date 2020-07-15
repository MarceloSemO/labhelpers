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


# fit 2D Gaussian to Greyscale png
# 'img' must be a matrix or a string specifying the filename
def fit_gauss_2d(img):
    if type(img) == str:
        img = str_to_img(img)
    xy_mesh = make_grid(img)
    # initial guess: use maximum
    max_pos = find_max_pos(img)
    p0 = (max_pos[1], max_pos[0], guess_sigma(img, "x", max_pos), guess_sigma(img, "y", max_pos), 1, 0)
    img_scaled = img/img.max()
    popt, pcov = opt.curve_fit(gauss2d_flat, xy_mesh, img_scaled.ravel(), p0=p0)
    return popt
