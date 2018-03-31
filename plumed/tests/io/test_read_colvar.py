
import os
import plumed.util.testing as tm
from plumed import read_colvar
from numpy.testing import assert_array_equal

DATA_PATH = tm.get_data_path()

class TestReadColvar(object):

    colvar_data = os.path.join(DATA_PATH, 'COLVAR')

    def test_column_names(self):
        df = read_colvar(self.colvar_data)
        desired_columns = ["time","v.x","v.y","v.z","d.x","d.y","d.z","d2","dist","distances.min","restraint.bias","restraint.force2"]
        assert_array_equal(df.columns.values, desired_columns)
