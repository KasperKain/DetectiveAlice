from utils.paths import resource_path


def load_map(path: str):
    with open(resource_path(path), "r", encoding="utf-8") as f:
        return [list(line.rstrip("\n")) for line in f]
