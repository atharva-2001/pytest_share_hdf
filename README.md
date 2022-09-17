### Pytest Share HDF
Pytest plugin to save references to an HDF file and then retrieve them for comparison with test results.
Use `tox` to run tests.

A proper test run should look like this:
```
==================================================================================== test session starts =====================================================================================
platform linux -- Python 3.8.13, pytest-7.1.3, pluggy-1.0.0
cachedir: .tox/py38/.pytest_cache
rootdir: /home/atharva/workspace/code/share_hdf
plugins: share-hdf-0.1.0
collected 7 items                                                                                                                                                                            

tests/test_share_hdf.py sssssss                                                                                                                                                        [100%]

===================================================================================== 7 skipped in 0.03s =====================================================================================
py38 run-test: commands[1] | pytest /home/atharva/workspace/code/share_hdf/tests --shared_hdf_generate
==================================================================================== test session starts =====================================================================================
platform linux -- Python 3.8.13, pytest-7.1.3, pluggy-1.0.0
cachedir: .tox/py38/.pytest_cache
rootdir: /home/atharva/workspace/code/share_hdf
plugins: share-hdf-0.1.0
collected 7 items                                                                                                                                                                            

tests/test_share_hdf.py .......                                                                                                                                                        [100%]

===================================================================================== 7 passed in 0.04s ======================================================================================
py38 run-test: commands[2] | pytest /home/atharva/workspace/code/share_hdf/tests --shared_hdf_compare
==================================================================================== test session starts =====================================================================================
platform linux -- Python 3.8.13, pytest-7.1.3, pluggy-1.0.0
cachedir: .tox/py38/.pytest_cache
rootdir: /home/atharva/workspace/code/share_hdf
plugins: share-hdf-0.1.0
collected 7 items                                                                                                                                                                            

tests/test_share_hdf.py .......                                                                                                                                                        [100%]

===================================================================================== 7 passed in 0.03s ======================================================================================
py38 run-test: commands[3] | pytest /home/atharva/workspace/code/share_hdf/tests --shared_hdf_generate --refdata_file_name=ref.hdf
==================================================================================== test session starts =====================================================================================
platform linux -- Python 3.8.13, pytest-7.1.3, pluggy-1.0.0
cachedir: .tox/py38/.pytest_cache
rootdir: /home/atharva/workspace/code/share_hdf
plugins: share-hdf-0.1.0
collected 7 items                                                                                                                                                                            

tests/test_share_hdf.py .......                                                                                                                                                        [100%]

===================================================================================== 7 passed in 0.02s ======================================================================================
py38 run-test: commands[4] | pytest /home/atharva/workspace/code/share_hdf/tests --shared_hdf_compare --refdata_file_name=ref.hdf
==================================================================================== test session starts =====================================================================================
platform linux -- Python 3.8.13, pytest-7.1.3, pluggy-1.0.0
cachedir: .tox/py38/.pytest_cache
rootdir: /home/atharva/workspace/code/share_hdf
plugins: share-hdf-0.1.0
collected 7 items                                                                                                                                                                            

tests/test_share_hdf.py .......                                                                                                                                                        [100%]

===================================================================================== 7 passed in 0.03s ======================================================================================

```