"""
File: conftest.py
Project: tests
Created Date: 17/10/2023
Author: Shun Suzuki
-----
Last Modified: 11/12/2023
Modified By: Shun Suzuki (suzuki@hapis.k.u-tokyo.ac.jp)
-----
Copyright (c) 2023 Shun Suzuki. All rights reserved.

"""


import pytest


def pytest_addoption(parser):
    parser.addoption("--soem", action="store_true", default=False, help="run soem tests")
    parser.addoption("--cuda", action="store_true", default=False, help="run cuda tests")
    parser.addoption("--gpu", action="store_true", default=False, help="run gpu tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "soem: soem tests")
    config.addinivalue_line("markers", "cuda: mark test as cuda test")
    config.addinivalue_line("markers", "gpu: mark test as gpu test")


def pytest_collection_modifyitems(session, config, items):
    option_lists = [
        ("--soem", "soem"),
        ("--cuda", "cuda"),
        ("--gpu", "gpu"),
    ]
    for option, marker in option_lists:
        if config.getoption(option):
            continue
        skip = pytest.mark.skip()
        for item in items:
            if marker in item.keywords:
                item.add_marker(skip)
