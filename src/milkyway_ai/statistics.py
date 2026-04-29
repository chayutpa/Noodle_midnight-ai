from __future__ import annotations

from collections.abc import Iterable

Number = float | int


def mean(values: Iterable[Number]) -> float:
    """Return the arithmetic mean of a non-empty sequence of numbers."""
    values_list = list(values)
    if not values_list:
        raise ValueError("mean() arg is an empty sequence")

    total = 0.0
    count = 0

    for value in values_list:
        if not isinstance(value, (int, float)):
            raise TypeError("mean() requires numeric values")
        total += float(value)
        count += 1

    return total / count
