import unittest
import os
import numpy as np

import labhelpers.Analysis.data_management as dm


class CameraTestCaseQuadratic(unittest.TestCase):
    def setUp(self) -> None:
        self.file_with_time_name = os.path.join(os.path.dirname(__file__), "test_data_timestamp.txt")
        self.file_with_time = open(self.file_with_time_name)
        self.file_no_time_name = os.path.join(os.path.dirname(__file__), "test_data_no_timestamp.txt")
        self.file_no_time = open(self.file_no_time_name)
        self.TIMESTAMP = 1596795859
        self.xvals = np.array([1.0, 2.0, 3.0])
        self.yvals = np.array([1.0, 1.5, 2.0])

    def test_get_header(self):
        self.assertEqual({"TIME": self.TIMESTAMP}, dm._get_header(self.file_with_time), "Did not read header of correctly")
        self.assertEqual({}, dm._get_header(self.file_no_time), "Did not read empty header correctly")

    def test_read_file(self):
        filenames = [self.file_with_time_name, self.file_no_time_name]
        for filename in filenames:
            result = dm.file_to_arrs(filename, ["Time_s", "Voltage_V"])
            if filename == self.file_with_time_name:
                self.assertEqual({'TIME': self.TIMESTAMP}, result[0])
            else:
                self.assertEqual({}, result[0])
            self.assertTrue((self.xvals == result[1][0]).all)
            self.assertTrue((self.yvals == result[1][1]).all)

    def tearDown(self) -> None:
        self.file_with_time.close()
        self.file_no_time.close()

