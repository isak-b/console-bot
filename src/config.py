import os
import yaml

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/"
cfg_path = os.path.join(root_path, "config.yaml")

with open(cfg_path, "r") as f:
    cfg = yaml.safe_load(f)


def save_cfg(cfg: dict) -> None:
    """Save config to file"""
    with open(cfg_path, "w") as f:
        yaml.dump(cfg, f)


def print_cfg(cfg: dict) -> None:
    """Print config to console"""
    print(yaml.dump(cfg))
