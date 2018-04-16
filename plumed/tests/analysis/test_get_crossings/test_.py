
import pandas as pd
import plumed.util.testing as tm
from plumed.analysis.transition_path_sampling import get_crossings

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

class TestGetCrossing(object):
    def test_number_of_crossings(self):
        barrier = 0.5
        df = get_crossings(test_data, barrier)
        assert len(df) == 2
        assert list(df.time.values) == [-1, 4]
