from os import environ

__all__ = ['PYTUMBLRX_FULL_COMPATIBILITY', 'PYTUMBLRX_REQUEST_JSON_ERROR']


def env_init(key, val_type, default=None):
    # Idea's taken from loguru
    val = environ.get(key)
    if val is None:
        return default
    if val_type == str:
        return val
    elif val_type == bool:
        if val.lower() in ("1", "true", "yes", "y", "ok", "on"):
            return True
        elif val.lower() in ("0", "false", "no", "n", "nok", "off", "-1"):
            return False
        raise ValueError(f"Invalid ENV VAR '{key}' (boolean expected): '{val}'")
    elif val_type == int:
        try:
            return int(val)
        except ValueError:
            raise ValueError(f"Invalid ENV VAR '{key}' (integer expected): '{val}'")


PYTUMBLRX_FULL_COMPATIBILITY = env_init("PYTUMBLRX_FULL_COMPATIBILITY", bool, False)
PYTUMBLRX_REQUEST_JSON_ERROR = env_init("PYTUMBLRX_REQUEST_JSON_ERROR", bool, False) or PYTUMBLRX_FULL_COMPATIBILITY
