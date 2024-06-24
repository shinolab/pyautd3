import pytest


def pytest_addoption(parser):
    parser.addoption("--soem", action="store_true", default=False, help="run soem tests")
    parser.addoption("--cuda", action="store_true", default=False, help="run cuda tests")
    parser.addoption("--gpu", action="store_true", default=False, help="run gpu tests")


def pytest_configure(config):
    config.addinivalue_line("markers", "soem: soem tests")
    config.addinivalue_line("markers", "cuda: cuda test")
    config.addinivalue_line("markers", "gpu: gpu test")


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
