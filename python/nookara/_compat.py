"""Old Velora and Bonfire names. They still work and say what to use instead."""
from __future__ import annotations

import warnings


def warn(old, new, stacklevel=3):
    warnings.warn(f"{old} is deprecated, use {new}", DeprecationWarning, stacklevel=stacklevel)


def renamed_method(old, new):
    def method(self, *args, **kwargs):
        warn(old, new)
        return getattr(self, new)(*args, **kwargs)
    method.__name__ = method.__qualname__ = old
    method.__doc__ = f"Deprecated: use ``{new}``."
    return method


def add_aliases(cls, pairs):
    for old, new in pairs.items():
        setattr(cls, old, renamed_method(old, new))


def renamed_attribute(old, new):
    def get(self):
        warn(old, new)
        return getattr(self, new)

    def set_(self, value):
        warn(old, new)
        setattr(self, new, value)
    return property(get, set_, doc=f"Deprecated: use ``{new}``.")


def legacy_kwarg(old_name, old_value, new_name, new_value, default):
    """Use the old keyword's value when it was given and the new one wasn't."""
    if old_value is None:
        return new_value
    warn(old_name + "=", new_name + "=", stacklevel=4)
    return old_value if new_value is default else new_value


def module_getattr(module_name, mapping, namespace):
    def __getattr__(name):
        if name in mapping:
            warn(name, mapping[name])
            return namespace[mapping[name]]
        raise AttributeError(f"module {module_name!r} has no attribute {name!r}")
    return __getattr__
