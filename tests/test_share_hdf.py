import numpy as np
import pandas as pd
import pytest


@pytest.mark.parametrize("n_points", [150, 200])
def test_arr_mul(n_points):
    arr = np.array([4, 5, 6]) * n_points
    return arr


@pytest.mark.share_hdf
@pytest.mark.parametrize("n_points", [150, 200])
def test_arr_mul2(n_points):
    arr = np.array([4, 5, 6]) * n_points
    return arr


@pytest.mark.share_hdf(name="testfoo")
class TestFoo:
    @pytest.mark.parametrize("n_points", [150, 200])
    def test_arr_mul3(self, n_points):
        arr = np.array([4, 5, 6]) * n_points
        return arr

    @pytest.mark.parametrize("n_points", [150, 200])
    def test_arr_mul4(self, n_points):
        arr = np.array([4, 5, 6]) * n_points
        return arr
    
    def test_pandas_df(self,):
        data = range(20)
        df = pd.DataFrame(data, columns=['Numbers'])
        return df
    
    # TODO
    def test_nothing(self):
        assert 2==2

