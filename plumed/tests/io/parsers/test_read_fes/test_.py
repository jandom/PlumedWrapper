
import os
import pytest
import plumed.util.testing as tm

from numpy import array
from numpy.testing import assert_array_equal, assert_array_almost_equal
from plumed import read_fes

DATA_PATH = tm.get_data_path()

class TestReadWham(object):
    wham_data = os.path.join(DATA_PATH, 'wham_result.dat')

    def test_columns(self):
        df = read_fes(self.wham_data)
        desired_columns = ['Window', 'Free', '+/-']
        assert_array_equal(df.columns.values, desired_columns)

    def test_valid_values(self):
        df = read_fes(self.wham_data)
        data = array([[0.00000000e+00, 0.00000000e+00, 0.00000000e+00],
                      [1.00000000e+00, -2.97664700e+00, 1.06520000e-02],
                      [2.00000000e+00, -8.43520000e-01, 1.85570000e-02],
                      [3.00000000e+00, 6.39616000e+00, 2.36410000e-02],
                      [4.00000000e+00, 1.87349430e+01, 2.58490000e-02],
                      [5.00000000e+00, 3.61598760e+01, 2.58150000e-02],
                      [6.00000000e+00, 5.86503310e+01, 2.60250000e-02],
                      [7.00000000e+00, 8.60749170e+01, 3.12030000e-02],
                      [8.00000000e+00, 1.08786612e+02, 6.95810000e-02],
                      [9.00000000e+00, 1.18055129e+02, 1.19232000e-01],
                      [1.00000000e+01, 1.19295804e+02, 1.73617000e-01],
                      [1.10000000e+01, 1.19326201e+02, 1.52721000e-01],
                      [1.20000000e+01, 1.19399530e+02, 1.46030000e-01],
                      [1.30000000e+01, 1.19844711e+02, 1.87421000e-01],
                      [1.40000000e+01, 1.20466334e+02, 1.89525000e-01],
                      [1.50000000e+01, 1.22303841e+02, 2.06086000e-01]
                     ])
        assert_array_almost_equal(df.values, data)
