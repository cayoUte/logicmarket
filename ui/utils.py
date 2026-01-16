
from types import SimpleNamespace


def props_to_obj(props_dict, defaults={}):
    merged = {**defaults, **props_dict}
    return SimpleNamespace(**merged)