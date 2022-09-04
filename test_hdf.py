from pandas import array
import pytest
import numpy as np
import tables

@pytest.mark.share_hdf
@pytest.mark.parametrize("n_points", [50, 100])
def test_arr_mul(
    n_points, refdata
):
    # reference data is used internally

    arr = np.array([1,2,3])*n_points
    return arr

@pytest.mark.share_hdf
@pytest.mark.parametrize("n_points", [150, 200])
def test_arr_mul2(
    n_points, refdata
):  
    arr = np.array([4,5,6])*n_points
    return arr


class TestFoo:
    ...

