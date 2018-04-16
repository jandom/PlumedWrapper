
import os
from numpy.testing import assert_almost_equal
import plumed.util.testing as tm

from plumed.io.parsers.bd import read_trajectories

DATA_PATH = tm.get_data_path()

class TestReadTrajectories(object):
    test_file = os.path.join(DATA_PATH, 'shot.dat')

    def test_read(self):
        files = (self.test_file,)
        trajectories = read_trajectories(files)
        keys = trajectories.keys()
        assert len(keys) == 1
        df = trajectories[self.test_file]

        assert df.time.values[0] == 0.0
        assert df.time.values[-1] == 0.0090

        assert_almost_equal(df.x.values[0], 0.5)
        assert_almost_equal(df.x.values[-1], 0.472)
