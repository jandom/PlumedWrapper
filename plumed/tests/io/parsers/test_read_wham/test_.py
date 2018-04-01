
import os
import io
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
import plumed.util.testing as tm
from plumed import read_wham

DATA_PATH = tm.get_data_path()

class TestReadFES(object):
    wham_data = os.path.join(DATA_PATH, 'wham_result.dat')
    wham_invalid_data = io.BytesIO("""#Coor		Free	+/-		Prob		+/-
    0.427930	inf	-nan
    0.432227	17.503672
        """)

    def test_columns(self):
        df = read_wham(self.wham_data)
        desired_columns = ['Coor', 'Free', 'FreeErr', 'Prob', 'ProbErr']
        assert_array_equal(df.columns.values, desired_columns)

    def test_valid_values(self):
        df = read_wham(self.wham_data)
        data = [
            [4.2793000e-01, np.inf, np.nan, 0.0000000e+00, 0.0000000e+00],
            [4.3222700e-01, 1.7503672e+01, 1.2748520e+00, 3.4100000e-04, 1.6700000e-04],
            [4.3652300e-01, 1.7500549e+01, np.nan, 3.4200000e-04, 2.3200000e-04],
            [4.4082000e-01, 1.3467288e+01, 5.8642400e-01, 1.3660000e-03, 2.7500000e-04],
            [4.4511700e-01, 1.0810190e+01, 1.4191300e-01, 3.4030000e-03, 2.0200000e-04],
            [4.4941400e-01, 9.2892150e+00, 3.8291000e-01, 5.7390000e-03, 6.6700000e-04]
        ]
        desired_values = np.array(data)
        assert_array_almost_equal(df.values, desired_values)

    def test_invalid_values(self):
        with pytest.raises(Exception) as excinfo:
            df = read_wham(self.wham_invalid_data)
        assert str(excinfo.value) == 'Length mismatch: Expected axis has 3 elements, new values have 5 elements'
