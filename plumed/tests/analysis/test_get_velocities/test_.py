
import pandas as pd
import plumed.util.testing as tm
from plumed.analysis.transition_path_sampling import get_velocities

DATA_PATH = tm.get_data_path()

test_data = pd.DataFrame([
    {'time': -2, 'x': 0.48},
    {'time': -1, 'x': 0.49},
    {'time': 0, 'x': 0.50}, # 1st crossing
    {'time': +1, 'x': 0.51},
    {'time': +2, 'x': 0.52},
    {'time': +3, 'x': 0.51},
    {'time': +4, 'x': 0.50}, # 2nd crossing
    {'time': +5, 'x': 0.49},
])

class TestGetVelocities(object):
    def test_exclude_zero_time(self):
        barrier = 0.5
        df = get_velocities(test_data, barrier)
        assert len(test_data) - 2 == len(df)
        assert (0 not in df.time.values)
        assert (1 in df.time.values)
