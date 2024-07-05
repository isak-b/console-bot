import os
import yaml

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"
cfg_path = os.path.join(ROOT_PATH, "config.yaml")


def load_cfg(path: str = cfg_path) -> dict:
    """Load config from file"""
    with open(path, "r") as f:
        cfg = yaml.safe_load(f)
    return cfg


def save_cfg(cfg: dict, path: str = cfg_path) -> None:
    """Save config to file"""
    with open(path, "w") as f:
        yaml.dump(cfg, f, sort_keys=False)
