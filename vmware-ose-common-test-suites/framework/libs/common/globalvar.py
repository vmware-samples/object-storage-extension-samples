from enum import Enum


def init():
    global _global_dict
    _global_dict = {}


def set_value(name, value):
    _global_dict[name] = value


def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue


class GlobalKeys(Enum):
    OSE_ARGS = 'ose_args'
    OSE_PROFILE_ARGS = 'ose_profile_args'
