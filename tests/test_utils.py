import os
import tempfile
import time
from datetime import datetime


from src.utils import save_cfg, load_cfg, load_files, get_time_separator


def test_save_load_cfg():
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file_path = temp_file.name

        # Test save_cfg
        cfg = {"some_key": "some_val", "paths": {"assistants": "some_dir/"}}
        save_cfg(cfg, temp_file_path)

        # Add config_dir
        cfg["paths"]["config_dir"] = os.path.dirname(temp_file_path)

        # Load cfg
        loaded_cfg = load_cfg(temp_file_path, make_paths_absolute=False)
        assert loaded_cfg == cfg


def test_relative_cfg_paths(cfg_path):
    config_dir = os.path.dirname(cfg_path)
    rel_paths = load_cfg(cfg_path=cfg_path, make_paths_absolute=False)["paths"]
    expected_paths = {
        "assistants": "assistants/",
        "history": "history/",
        "config_dir": config_dir,
    }
    assert len(rel_paths) == len(expected_paths)
    for expected_key, expected_path in expected_paths.items():
        assert expected_key in rel_paths
        assert rel_paths[expected_key] == expected_path


def test_absolute_cfg_paths(cfg_path):
    config_dir = os.path.dirname(cfg_path)
    abs_paths = load_cfg(cfg_path=cfg_path, make_paths_absolute=True)["paths"]
    expected_paths = {
        "assistants": os.path.join(config_dir, "assistants/"),
        "history": os.path.join(config_dir, "history/"),
        "config_dir": config_dir,
    }
    assert len(abs_paths) == len(expected_paths)
    for expected_key, expected_path in expected_paths.items():
        assert expected_key in abs_paths
        assert abs_paths[expected_key] == expected_path


def test_load_assistants(cfg):
    assistants = load_files(path=cfg["paths"]["assistants"])
    expected_assistants = {"MockBot": "foo bar"}
    assert len(assistants) == len(expected_assistants)
    for expected_bot, expected_instruction in expected_assistants.items():
        assert expected_bot in assistants
        assert expected_instruction == assistants[expected_bot]


def test_get_time_separator():
    current_date = datetime(2024, 7, 14, 23, 59, 59)
    event_dates = {
        datetime(2024, 7, 14, 23, 59, 59): "Today",
        datetime(2024, 7, 14, 0, 0, 0): "Today",
        datetime(2024, 7, 13, 23, 59, 59): "Yesterday",
        datetime(2024, 7, 13, 0, 0, 0): "Yesterday",
        datetime(2024, 7, 12, 23, 59, 59): "This week",
        datetime(2024, 7, 8, 0, 0, 0): "This week",
        datetime(2024, 7, 7, 23, 59, 59): "This month",
        datetime(2024, 7, 1, 0, 0, 0): "This month",
        datetime(2024, 6, 30, 23, 59, 59): "June",
        datetime(2024, 1, 1, 0, 0, 0): "January",
        datetime(2023, 12, 31, 23, 59, 59): "2023",
    }

    for event_date, expected in event_dates.items():
        result = get_time_separator(event_date, current_date)
        assert result == expected, f"{event_date} vs. {current_date}\n- {expected=}\n- {result=}"
