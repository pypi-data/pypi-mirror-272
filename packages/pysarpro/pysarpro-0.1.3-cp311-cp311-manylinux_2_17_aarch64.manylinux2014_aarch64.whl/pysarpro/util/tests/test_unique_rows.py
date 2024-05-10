import numpy as np
from pysarpro._shared import testing
from pysarpro._shared.testing import assert_equal
from pysarpro.util import unique_rows


def test_discontiguous_array():
    ar = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]], np.uint8)
    ar = ar[::2]
    ar_out = unique_rows(ar)
    desired_ar_out = np.array([[1, 0, 1]], np.uint8)
    assert_equal(ar_out, desired_ar_out)


def test_uint8_array():
    ar = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]], np.uint8)
    ar_out = unique_rows(ar)
    desired_ar_out = np.array([[0, 1, 0], [1, 0, 1]], np.uint8)
    assert_equal(ar_out, desired_ar_out)


def test_float_array():
    ar = np.array([[1.1, 0.0, 1.1], [0.0, 1.1, 0.0], [1.1, 0.0, 1.1]], float)
    ar_out = unique_rows(ar)
    desired_ar_out = np.array([[0.0, 1.1, 0.0], [1.1, 0.0, 1.1]], float)
    assert_equal(ar_out, desired_ar_out)


def test_1d_array():
    ar = np.array([1, 0, 1, 1], np.uint8)
    with testing.raises(ValueError):
        unique_rows(ar)


def test_3d_array():
    ar = np.arange(8).reshape((2, 2, 2))
    with testing.raises(ValueError):
        unique_rows(ar)
