import os
import tempfile

from src.utils import save_cfg, load_cfg, load_bots


def test_save_load_cfg():
    with tempfile.NamedTemporaryFile() as temp_file:
        temp_file_path = temp_file.name

        # Test save_cfg
        cfg = {"some_key": "some_val", "paths": {"bots": "some_dir/"}}
        save_cfg(cfg, temp_file_path)

        # Add config_dir
        cfg["paths"]["config_dir"] = os.path.dirname(temp_file_path)

        # Load cfg
        loaded_cfg = load_cfg(temp_file_path, make_paths_absolute=False)
        assert loaded_cfg == cfg


def test_relative_cfg_paths(cfg_path):
    config_dir = os.path.dirname(cfg_path)
    rel_paths = load_cfg(cfg_path=cfg_path, make_paths_absolute=False)["paths"]
    expected_paths = {"bots": "bots/", "config_dir": config_dir}
    assert len(rel_paths) == len(expected_paths)
    for expected_key, expected_path in expected_paths.items():
        assert expected_key in rel_paths
        assert rel_paths[expected_key] == expected_path


def test_absolute_cfg_paths(cfg_path):
    config_dir = os.path.dirname(cfg_path)
    abs_paths = load_cfg(cfg_path=cfg_path, make_paths_absolute=True)["paths"]
    expected_paths = {"bots": os.path.join(config_dir, "bots/"), "config_dir": config_dir}
    assert len(abs_paths) == len(expected_paths)
    for expected_key, expected_path in expected_paths.items():
        assert expected_key in abs_paths
        assert abs_paths[expected_key] == expected_path


def test_load_bots(cfg):
    bots = load_bots(bots_path=cfg["paths"]["bots"])
    expected_bots = {"MockBot": "foo bar"}
    assert len(bots) == len(expected_bots)
    for expected_bot, expected_instruction in expected_bots.items():
        assert expected_bot in bots
        assert expected_instruction == bots[expected_bot]
