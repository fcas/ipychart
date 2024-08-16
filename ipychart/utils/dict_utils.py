from collections.abc import Mapping
from typing import Any, Dict


def has(obj: Dict[str, Any], keys: str) -> bool:
    """
    Check if a nested key exists in a dictionary.

    Args:
        obj (Dict[str, Any]): The dictionary to check.
        keys (str): A string representing the nested key(s), separated by dots.

    Returns:
        bool: True if the nested key exists, False otherwise.

    Example:
        >>> d = {"a": {"b": {"c": 1}}}
        >>> has_key(d, "a.b.c")
        True
        >>> has_key(d, "a.b.d")
        False
    """
    for key in keys.split('.'):
        if isinstance(obj, dict) and key in obj:
            obj = obj[key]
        else:
            return False
    return True

def merge(d1: Dict[str, Any], d2: Mapping) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries.

    Args:
        d1 (Dict[str, Any]): The dictionary to merge into.
        d2 (Mapping): The dictionary with values to merge.

    Returns:
        Dict[str, Any]: The merged dictionary.

    Example:
        >>> d1 = {"a": {"b": 1}}
        >>> d2 = {"a": {"c": 2}}
        >>> deep_merge(d1, d2)
        {'a': {'b': 1, 'c': 2}}
    """
    for k, v in d2.items():
        if k in d1 and isinstance(d1[k], dict) and isinstance(v, Mapping):
            merge(d1[k], v)
        else:
            d1[k] = v
    return d1

def set_(d: Dict[str, Any], keys: str, value: Any) -> None:
    """
    Set a value in a nested dictionary.

    Args:
        d (Dict[str, Any]): The dictionary in which to set the value.
        keys (str): A string representing the nested key(s), separated by dots.
        value (Any): The value to set at the specified nested key.

    Example:
        >>> d = {"a": {"b": {}}}
        >>> set_nested_item(d, "a.b.c", 1)
        >>> d
        {'a': {'b': {'c': 1}}}
    """
    keys = keys.split('.')
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value