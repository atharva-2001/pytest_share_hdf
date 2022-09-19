from collections.abc import Iterable
from functools import wraps

import numpy as np
import pandas as pd
import pytest
import tables


class Reference:
    def __init__(self, config=None) -> None:
        self.config = config
        self.fname = self.config.getoption("--refdata_file_name")
        self.setup()

    def setup(self):
        if self.config.getoption("--shared_hdf_generate"):
            self.option = "generate"
            self.tables_file = tables.open_file(self.fname, "w")
            self.store_file = pd.HDFStore(self.fname, mode="a")
        elif self.config.getoption("--shared_hdf_compare"):
            self.option = "compare"
            self.tables_file = tables.open_file(self.fname, "r")
            self.store_file = pd.HDFStore(self.fname, mode="r")
        else:
            self.option = None
            self.tables_file = None
            self.store_file = None

    def teardown(self):
        self.store_file.close()
        self.tables_file.close()


reference_key = pytest.StashKey[Reference]()


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption("--shared_hdf_generate", action="store_true", help="")
    group.addoption("--shared_hdf_compare", action="store_true", help="")
    group.addoption(
        "--refdata_file_name", action="store", default="reference.hdf", help=""
    )


def pytest_collection_modifyitems(session, config, items):
    # TODO use pytest_sessionstart instead?
    if not config.getoption("--shared_hdf_generate") and not config.getoption(
        "--shared_hdf_compare"
    ):
        for item in items:
            if item.get_closest_marker("share_hdf"):
                item.add_marker(pytest.mark.skip)
    else:
        session.stash[reference_key] = Reference(config=config)


def pytest_sessionfinish(session):
    reference = session.stash.get(reference_key, None)
    if reference is not None:
        reference.teardown()


class ArrayComparisonHDF:
    def __init__(
        self,
        config,
        refdata=None,
    ):
        self.config = config
        self.refdata = refdata

    def pytest_runtest_setup(self, item):
        compare = item.get_closest_marker("share_hdf")
        session = item.session

        if compare is None:
            return
        else:
            self.reference = session.stash[reference_key]
            self.refdata = self.reference.tables_file
            self.store_refdata = self.reference.store_file

        self.group_where = compare.kwargs.get("where", self.refdata.root)
        self.group_name = compare.kwargs.get("name", None)

        original = item.function

        @wraps(item.function)
        def item_function_wrapper(*args, **kwargs):
            leaf_name = item.name
            leaf_name = leaf_name.replace("[", "_").replace("]", "_")

            data = original(*args, **kwargs)

            if data is None:
                return

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
                if isinstance(data, pd.DataFrame):
                    self.store_refdata.put(key=leaf_name, value=data)
                elif isinstance(data, Iterable):
                    self.refdata.create_carray(group, name=leaf_name, obj=data)

            if self.config.getoption("--shared_hdf_compare"):
                group = self.refdata.get_node(
                    where=self.group_where, name=self.group_name
                )
                if isinstance(data, pd.DataFrame):
                    pd.testing.assert_frame_equal(
                        data,
                        self.store_refdata[leaf_name],
                    )
                elif isinstance(data, Iterable):
                    np.testing.assert_allclose(
                        data,
                        self.refdata.get_node(group, name=leaf_name),
                    )

        if item.cls is not None:
            setattr(item.cls, item.function.__name__, item_function_wrapper)
        else:
            item.obj = item_function_wrapper


def pytest_configure(
    config,
):
    config.getini("markers").append("share_hdf")
    config.pluginmanager.register(
        ArrayComparisonHDF(
            config,
        ),
        name="pytest_share_hdf",
    )
