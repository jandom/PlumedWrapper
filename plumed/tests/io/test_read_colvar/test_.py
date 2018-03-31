
import os
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal

import plumed.util.testing as tm
from plumed import read_colvar



DATA_PATH = tm.get_data_path()

class TestReadColvar(object):
    colvar_missing_header_data = os.path.join(DATA_PATH, 'COLVAR_MISSING-HEADER')
    colvar_header_value_mismatch_data = os.path.join(DATA_PATH, 'COLVAR_HEADER-VALUE-MISMATCH')
    colvar_short_data = os.path.join(DATA_PATH, 'COLVAR_SHORT')

    def test_file_does_not_exits(self):
        with pytest.raises(Exception) as excinfo:
            df = read_colvar('file_does_not_exist')
        assert str(excinfo.value) == "[Errno 2] No such file or directory: 'file_does_not_exist'"

    def test_column_missing(self):
        with pytest.raises(Exception) as excinfo:
            df = read_colvar(self.colvar_missing_header_data)
        assert str(excinfo.value) == 'Missing or incorrect header'

    def test_column_names(self):
        df = read_colvar(self.colvar_short_data)
        desired_columns = ["time", "v.x", "v.y", "v.z", "d.x", "d.y", "d.z", "d2", \
            "dist", "distances.min", "restraint.bias", "restraint.force2"]
        assert_array_equal(df.columns.values, desired_columns)

    def test_column_value_mismatch(self):
        with pytest.raises(Exception) as excinfo:
            df = read_colvar(self.colvar_header_value_mismatch_data)
        assert str(excinfo.value) == 'Length mismatch: Expected axis has 12 elements, new values have 10 elements'

    def test_values(self):
        df = read_colvar(self.colvar_short_data)
        data = [[0.00000000e+00, -1.64080600e+00, -2.90569000e-01,
                 -1.76075800e+00, -3.79829900e+00, 2.50386100e+00,
                 -3.30397500e+00, 1.09162520e+01, 3.30397500e+00,
                 4.73081000e-01, 2.67042200e+00, 5.34084481e+03],
                [3.00000000e+01, -1.62970900e+00, -4.24727000e-01,
                 -1.78493700e+00, 2.82404800e+00, -2.40071900e+00,
                 -3.35808400e+00, 1.12767290e+01, 3.35808400e+00,
                 5.01038000e-01, 5.10430200e+00, 1.02086043e+04]]
        desired_values = np.array(data)
        assert_array_almost_equal(df.values, desired_values, decimal=4)
