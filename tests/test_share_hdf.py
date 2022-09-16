import numpy as np
import pandas as pd
import pytest

# TODO: this is probably not needed anymore
# @pytest.mark.parametrize("n_points", [150, 200])
# def test_arr_mul(n_points):
#     arr = np.array([4, 5, 6]) * n_points
#     return arr

def test_marker(pytester):
    """Make sure that share_hdf marker works."""
    
    # makeconftest is something
    pytester.makepyfile(
        """
        import pytest
        import numpy as np

        @pytest.mark.share_hdf
        @pytest.mark.parametrize("nums", [150, 200])
        def test_arr(nums):
            arr = np.array([4, 5, 6]) * nums
            return arr
        """
    )

    result = pytester.runpytest(
        '--shared_hdf_generate=.',
    )
    result.assert_outcomes(passed=2)
    
    result = pytester.runpytest(
        '--shared_hdf_compare=.',
    )
    result.assert_outcomes(passed=2)


# @pytest.mark.share_hdf(name="testfoo")
# class TestFoo:
#     @pytest.mark.parametrize("n_points", [150, 200])
#     def test_arr_mul3(self, n_points):
#         arr = np.array([4, 5, 6]) * n_points
#         return arr

#     @pytest.mark.parametrize("n_points", [150, 200])
#     def test_arr_mul4(self, n_points):
#         arr = np.array([4, 5, 6]) * n_points
#         return arr
    
#     def test_pandas_df(self,):
#         data = range(20)
#         df = pd.DataFrame(data, columns=['Numbers'])
#         return df
    
#     # TODO
#     def test_nothing(self):
#         assert 2==2

