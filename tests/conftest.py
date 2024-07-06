import os
import sys

import pytest

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG_PATH = f"{ROOT_PATH}/tests/test_profile/config.yaml"
sys.path.insert(0, ROOT_PATH)

from src.utils import load_cfg  # noqa: E402

test_cfg = load_cfg(CFG_PATH)


@pytest.fixture(scope="session")
def root_path():
    return ROOT_PATH


@pytest.fixture(scope="session")
def cfg():
    return test_cfg


@pytest.fixture(scope="session")
def cfg_path():
    return CFG_PATH
