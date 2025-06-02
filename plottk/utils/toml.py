import tomllib


def load_toml(filename) -> dict:
    with open(filename, 'rb') as f:
        return tomllib.load(f)
