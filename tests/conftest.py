import os
import sys

import pytest

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
sys.path.insert(0, root_path)

from src.config import load_cfg

test_cfg = load_cfg()


@pytest.fixture(scope="session")
def cfg():
    return test_cfg
