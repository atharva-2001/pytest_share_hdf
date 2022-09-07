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
    ):
        self.config = config
        self.refdata = refdata

    def pytest_runtest_setup(self, item):
        compare = item.get_closest_marker("share_hdf")
        if compare is None:
            return
        else:
            # TODO: find alternative
            self.refdata = item._request.getfixturevalue("refdata")

        self.group_where = compare.kwargs.get("where", self.refdata.root)
        self.group_name = compare.kwargs.get("name", None)

        original = item.function

        @wraps(item.function)
        def item_function_wrapper(*args, **kwargs):
            leaf_name = item.name
            leaf_name = leaf_name.replace("[", "_").replace("]", "_")

            data = original(*args, **kwargs)

            if self.group_name is None:
                group = self.refdata.root

            if self.config.getoption("--shared_hdf_generate"):
                if self.group_name is not None:
                    try:
                        group = self.refdata.create_group(
                            where=self.group_where, name=self.group_name
                        )
                    except tables.NodeError:
                        group = self.refdata.get_node(
                            where=self.group_where, name=self.group_name
                        )
                if isinstance(data, Iterable):
                    self.refdata.create_carray(group, name=leaf_name, obj=data)

            if self.config.getoption("--shared_hdf_compare"):
                group = self.refdata.get_node(
                    where=self.group_where, name=self.group_name
                )
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
