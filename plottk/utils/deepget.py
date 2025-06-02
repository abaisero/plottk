def deepget_keylist(config: dict, keys: list[str], *, default=None):
    key, *keys = keys

    if not keys:
        return config.get(key, default)

    try:
        config = config[key]
    except KeyError:
        return default

    return deepget_keylist(config, keys, default=default)


def deepget(config: dict, key: str, *, default=None):
    keys = key.split('.')
    return deepget_keylist(config, keys, default=default)
