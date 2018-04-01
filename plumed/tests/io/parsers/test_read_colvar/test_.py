
import os
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
import plumed.util.testing as tm
from plumed import read_colvar

import io

DATA_PATH = tm.get_data_path()

class TestReadColvar(object):
    colvar_short_data = os.path.join(DATA_PATH, 'COLVAR')

    def test_file_does_not_exits(self):
        with pytest.raises(Exception) as excinfo:
            df = read_colvar('file_does_not_exist')
        assert str(excinfo.value) == "[Errno 2] No such file or directory: 'file_does_not_exist'"

    def test_column_missing(self):
        file_contents = io.BytesIO(b""" 0.000000 -1.640806 -0.290569 -1.760758 -3.798299 2.503861 -3.303975 10.916252 3.303975 0.473081 2.670422 5340.844815
         29.999999 -1.629709 -0.424727 -1.784937 2.824048 -2.400719 -3.358084 11.276729 3.358084 0.501038 5.104302 10208.604324
         """)
        with pytest.raises(Exception) as excinfo:
            df = read_colvar(file_contents)
        assert str(excinfo.value) == 'Missing or incorrect header'

    def test_column_names(self):
        df = read_colvar(self.colvar_short_data)
        desired_columns = ["time", "v.x", "v.y", "v.z", "d.x", "d.y", "d.z", "d2", \
            "dist", "distances.min", "restraint.bias", "restraint.force2"]
        assert_array_equal(df.columns.values, desired_columns)

    def test_column_value_mismatch(self):
        file_contents = io.BytesIO(b"""#! FIELDS time v.x v.y v.z d.x d.y d.z d2 dist distances.min
         0.000000 -1.640806 -0.290569 -1.760758 -3.798299 2.503861 -3.303975 10.916252 3.303975 0.473081 2.670422 5340.844815
         29.999999 -1.629709 -0.424727 -1.784937 2.824048 -2.400719 -3.358084 11.276729 3.358084 0.501038 5.104302 10208.604324
         """)

        with pytest.raises(Exception) as excinfo:
            df = read_colvar(file_contents)
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
