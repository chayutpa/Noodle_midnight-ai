import pytest

from milkyway_ai import mean


def test_mean_returns_average_for_numbers():
    assert mean([1, 2, 3, 4, 5]) == 3.0


def test_mean_accepts_float_values():
    assert mean([1.5, 2.5, 3.0]) == pytest.approx(2.3333333333333335)


def test_mean_raises_value_error_for_empty_sequence():
    with pytest.raises(ValueError):
        mean([])


def test_mean_raises_type_error_for_non_numeric_values():
    with pytest.raises(TypeError):
        mean([1, "two", 3])
