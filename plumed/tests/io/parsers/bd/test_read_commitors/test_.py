
import os
import io
import pytest
import numpy as np
import pandas as pd
from numpy.testing import assert_array_equal, assert_array_almost_equal

from plumed.io.parsers.bd import read_commitorrs

class TestReadCommitors(object):
    def test_read(self):
        basinA = 0.1
        basinB = 1.0
        data = {
            'none': pd.DataFrame([
                {'time': 0.0, 'x': 0.5},
                {'time': 0.1, 'x': 0.5},
            ]),
            'onlyA': pd.DataFrame([
                {'time': 0.0, 'x': 0.5},
                {'time': 0.1, 'x': 0.0},
            ]),
            'onlyB': pd.DataFrame([
                {'time': 0.0, 'x': 0.5},
                {'time': 0.1, 'x': 1.0},           
            ]),
        }
        committors = read_commitorrs(data, basinA, basinB)
        keys = committors.keys()
        assert len(keys) == 3
        assert committors['none'] == None
        assert committors['onlyA'] == 'A'
        assert committors['onlyB'] == 'B'
