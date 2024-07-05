import os
import sys

import pytest

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
sys.path.insert(0, ROOT_PATH)

from chat.utils import load_cfg  # noqa: E402

test_cfg = load_cfg()


@pytest.fixture(scope="session")
def root_path():
    return ROOT_PATH


@pytest.fixture(scope="session")
def cfg():
    return test_cfg
