import yaml


def get_formatted_dict(d: dict, highlight_keys: list = None):
    formatted_dict = "\n"
    for line in yaml.dump(d, default_flow_style=False, sort_keys=False).split("\n"):
        if highlight_keys:
            if any([line.lstrip().startswith(f"{key}:") for key in highlight_keys]):
                line = f"<b><ansicyan>{line}</ansicyan></b>"
            else:
                line = f"<ansigray>{line}</ansigray>"
        formatted_dict += f"{line}\n"
    formatted_dict = formatted_dict.rstrip("\n")
    return formatted_dict
