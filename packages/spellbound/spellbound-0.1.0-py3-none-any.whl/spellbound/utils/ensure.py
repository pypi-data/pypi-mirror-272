from collections.abc import Iterable


def ensure_list(value):
    """
    Ensure that `value` is a list.

    Args:
        value (Any): input value

    Returns:
        List: value converted to a list if it is not already a list
    """
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if not isinstance(value, (str, dict)) and isinstance(
        value, Iterable
    ):
        return list(value)
    return [value]

