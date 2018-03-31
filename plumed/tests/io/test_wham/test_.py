
import os
import pytest
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
import plumed.util.testing as tm
from plumed import read_wham

import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

DATA_PATH = tm.get_data_path()

class TestReadWham(object):
    wham_data = os.path.join(DATA_PATH, 'result.dat')

    def test_read_wham(self):
        df = read_wham(self.wham_data)
        desired_columns = ['Coor', 'Free', 'FreeErr', 'Prob', 'ProbErr']
        assert_array_equal(df.columns.values, desired_columns)
