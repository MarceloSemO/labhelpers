import unittest
import numpy as np
import labhelpers.Analysis.functions as func


class FunctionsTestCase(unittest.TestCase):
    def test_gauss_2d(self):
        semi_grid_size = 3
        sigma_x = 1
        sigma_y = 1
        x = np.linspace(-semi_grid_size, semi_grid_size, num=2 * semi_grid_size + 1)
        y = x

        # test for complete grid
        self.x, self.y = np.meshgrid(x, y)
        expected = np.exp(-2 * (self.x**2 + self.y**2))
        gauss2d = func.gauss2d((x, y), 0, 0, sigma_x, sigma_y, 1, 0)
        self.assertTrue(np.allclose(gauss2d, expected), f"2D Gaussian grid not computed correctly.\n"
                                                        f"Result is:{gauss2d}. Expected:{expected}")
        # test for single value
        x1 = 2
        y1 = 1
        expected = np.exp(-2 * (x1**2 + y1**2))
        gauss2d = func.gauss2d((x1, y1), 0, 0, sigma_x, sigma_y, 1, 0)
        self.assertAlmostEqual(expected, gauss2d, "Calculated value differs from expected.")

