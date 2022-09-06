import numpy as np
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


@pytest.mark.share_hdf
class TestFoo:
    @pytest.mark.parametrize("n_points", [150, 200])
    def test_arr_mul3(self, n_points):
        arr = np.array([4, 5, 6]) * n_points
        return arr
