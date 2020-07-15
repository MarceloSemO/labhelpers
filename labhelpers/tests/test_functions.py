import unittest
import numpy as np
import labhelpers.Analysis.functions as func


class FunctionsTestCase(unittest.TestCase):
    def test_gauss_2d_quadratic(self):
        semi_grid_size = 3
        sigma_x = 1
        sigma_y = 1
        x = np.linspace(-semi_grid_size, semi_grid_size, num=2 * semi_grid_size + 1)
        y = x

        # test for complete grid
        self.xy = np.meshgrid(x, y)
        expected = np.exp(-2 * (self.xy[0]**2 + self.xy[1]**2))
        gauss2d = func.gauss2d(self.xy, 0, 0, sigma_x, sigma_y, 1, 0)
        self.assertTrue(np.allclose(gauss2d, expected), f"2D Gaussian grid not computed correctly.\n"
                                                        f"Result is:{gauss2d}. Expected:{expected}")
        # test for single value
        x1 = 2
        y1 = 1
        expected = np.exp(-2 * (x1**2 + y1**2))
        gauss2d = func.gauss2d((x1, y1), 0, 0, sigma_x, sigma_y, 1, 0)
        self.assertAlmostEqual(expected, gauss2d, "Calculated value differs from expected.")

    def test_gauss_2d_non_quadratic(self):
        semi_grid_size_x = 3
        semi_grid_size_y = 5
        sigma_x = 1
        sigma_y = 2
        x = np.linspace(-semi_grid_size_x, semi_grid_size_x, num=2 * semi_grid_size_x + 1)
        y = np.linspace(-semi_grid_size_y, semi_grid_size_y, num=2 * semi_grid_size_x + 1)

        # test for complete grid
        self.xy = np.meshgrid(x, y)
        expected = np.exp(-2 * (self.xy[0]**2 + self.xy[1]**2/4))
        gauss2d = func.gauss2d(self.xy, 0, 0, sigma_x, sigma_y, 1, 0)
        self.assertTrue(np.allclose(gauss2d, expected), f"2D Gaussian grid not computed correctly.\n"
                                                        f"Result is:{gauss2d}. Expected:{expected}")
        # test for single value
        x1 = 2
        y1 = 1
        expected = np.exp(-2 * (x1**2 + y1**2/4))
        gauss2d = func.gauss2d((x1, y1), 0, 0, sigma_x, sigma_y, 1, 0)
        self.assertAlmostEqual(expected, gauss2d, "Calculated value differs from expected.")