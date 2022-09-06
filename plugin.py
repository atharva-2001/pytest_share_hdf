from collections import Iterable
from functools import wraps

import numpy as np
import pandas as pd
import pytest
import tables


@pytest.fixture(scope="session")
def refdata(request):
    fname = request.config.getoption("--refdata_file_name")
    if not fname:
        fname = "reference.hdf"

    if request.config.getoption("--shared_hdf_generate"):
        hdf_file = tables.open_file(fname, "w")
    elif request.config.getoption("--shared_hdf_compare"):
        hdf_file = tables.open_file(fname, "r")

    yield hdf_file
    hdf_file.close()


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption("--shared_hdf_generate", action="store", help="")
    group.addoption("--shared_hdf_compare", action="store", help="")
    group.addoption("--refdata_file_name", action="store", help="")


def pytest_collection_modifyitems(config, items):
    # TODO need to reconsider this function's necessity
    for item in items:
        if item.get_closest_marker("share_hdf"):
            item.fixturenames.append("refdata")


class ArrayComparisionHDF:
    def __init__(
        self,
        config,
        refdata=None,
        group=None,
        generate=True,
        compare=False,
    ):
        self.config = config
        self.refdata = refdata
        self.group = group
        self.compare = compare
        self.generate = generate

    def pytest_runtest_setup(self, item):
        compare = item.get_closest_marker("share_hdf")
        if compare is None:
            return
        else:
            self.refdata = item._request.getfixturevalue("refdata")
        original = item.function

        @wraps(item.function)
        def item_function_wrapper(*args, **kwargs):
            leaf_name = item.name
            leaf_name = leaf_name.replace("[", "_").replace("]", "_")

            data = original(*args, **kwargs)

            if self.group is None:
                # TODO
                group = self.refdata.root
            else:
                group = self.refdata.get_node(
                    group,
                )

            if self.config.getoption("--shared_hdf_generate"):
                # save array as a leaf?
                if isinstance(data, Iterable):
                    self.refdata.create_carray(group, name=leaf_name, obj=data)
            if self.config.getoption("--shared_hdf_compare"):
                np.testing.assert_allclose(
                    data,
                    self.refdata.get_node(group, name=leaf_name),
                )

        if item.cls is not None:
            setattr(item.cls, item.function.__name__, item_function_wrapper)
        else:
            item.obj = item_function_wrapper


def pytest_configure(config):
    config.pluginmanager.register(
        ArrayComparisionHDF(
            config,
        ),
        name="pytest_share_hdf",
    )
