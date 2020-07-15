import unittest
import numpy as np
import labhelpers.Analysis.camera as cam
from labhelpers.Analysis.functions import gauss2d


class CameraTestCase(unittest.TestCase):
    def setUp(self):
        self.grid_size = 101
        self.sigma_x = 10
        self.sigma_y = 10
        x = np.linspace(0, self.grid_size-1, num=self.grid_size)
        y = x
        self.x_center = np.floor(self.grid_size/2)
        self.y_center =np.floor(self.grid_size/2)
        self.gauss2d = gauss2d((x, y),
                               self.x_center, self.y_center,
                               self.sigma_x, self.sigma_y,
                               1, 0)

    def test_gauss2d_max(self):
        self.assertEqual((self.x_center, self.y_center), cam.find_max_pos(self.gauss2d),
                         'Did not find correct maximum')

    def test_sigma_guess(self):
        self.assertEqual(self.sigma_x, cam.guess_sigma(self.gauss2d, "x"))

    def test_fit_gauss2d(self):
        self.assertTrue(np.allclose([50, 50, self.sigma_x, self.sigma_y, 1, 0], cam.fit_gauss_2d(self.gauss2d)),
                        f"{cam.fit_gauss_2d(self.gauss2d)}")
