import os
import yaml

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DEFAULT_CFG_PATH = os.path.join(ROOT_PATH, "config.yaml")


def load_cfg(cfg_path: str = DEFAULT_CFG_PATH, make_paths_absolute: bool = True) -> dict:
    """Load config from file"""
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    cfg["paths"]["config_dir"] = os.path.dirname(cfg_path)
    if make_paths_absolute is True:
        for dir_name, dir_path in cfg["paths"].items():
            cfg["paths"][dir_name] = os.path.join(cfg["paths"]["config_dir"], dir_path)
    return cfg


def save_cfg(cfg: dict, path: str = DEFAULT_CFG_PATH) -> None:
    """Save config to file"""
    with open(path, "w") as f:
        yaml.dump(cfg, f, sort_keys=False)


def load_bots(bots_path: str) -> dict:
    """Load bots from files"""
    bots = {}
    for filename in os.listdir(bots_path):
        file_path = os.path.join(bots_path, filename)
        with open(file_path, "r") as f:
            bots[filename.removesuffix(".txt")] = f.read()
    return bots
