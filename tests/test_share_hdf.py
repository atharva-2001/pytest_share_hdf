import numpy as np
import pandas as pd
import pytest


@pytest.mark.share_hdf
@pytest.mark.parametrize("nums", [150, 200])
def test_arr(nums):
    arr = np.array([4, 5, 6]) * nums
    return arr


@pytest.mark.share_hdf
def test_pandas_df_sep():
    data = range(20)
    df = pd.DataFrame(data, columns=["Numbers"])
    return df


@pytest.mark.share_hdf
class TestFoo:
    @pytest.mark.parametrize("n_points", [150, 200])
    def test_arr_grp(self, n_points):
        arr = np.array([4, 5, 6]) * n_points
        return arr

    def test_pandas_grp(self):
        data = range(20)
        df = pd.DataFrame(data, columns=["Numbers"])
        return df

    # TODO
    def test_nothing(self):
        assert 2 == 2
