
import pandas as pd
from numpy.testing import assert_almost_equal

from plumed.io.parsers.bd import concatenate_trajectories

class TestConcatenateTrajectories(object):
    forward_trajectory = pd.DataFrame([
        {'time': 0.0, 'x': 0.1},
        {'time': 0.1, 'x': 0.2},
    ])

    backward_trajectory = pd.DataFrame([
        {'time': 0.0, 'x': 0.1},
        {'time': 0.1, 'x': 0.0},
    ])

    def test_concatenate_trajectories(self):
        df = concatenate_trajectories(self.forward_trajectory, self.backward_trajectory)
        assert len(df) == 4
        assert list(df.time.values) == [-0.1, -0.0, 0.0, 0.1]
