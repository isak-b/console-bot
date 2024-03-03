import io
import tempfile
from contextlib import redirect_stdout

from src.config import save_cfg, load_cfg

buffer = io.StringIO()


def test_config():
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file_path = temp_file.name

        # Test save_cfg
        cfg = {"key_a": "val_a"}
        save_cfg(cfg, temp_file_path)

        # Test load_cfg
        loaded_cfg = load_cfg(temp_file_path)
        assert loaded_cfg == cfg
