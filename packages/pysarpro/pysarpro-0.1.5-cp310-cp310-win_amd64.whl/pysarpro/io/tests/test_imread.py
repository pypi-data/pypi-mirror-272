from tempfile import NamedTemporaryFile

import numpy as np
from pytest import importorskip

from pysarpro._shared.testing import TestCase, assert_array_almost_equal
from pysarpro.io import imread, imsave, reset_plugins, use_plugin

importorskip('imread')


def setup():
    use_plugin('imread')


def teardown():
    reset_plugins()


class TestSave(TestCase):
    def roundtrip(self, x, scaling=1):
        with NamedTemporaryFile(suffix='.png') as f:
            fname = f.name

        imsave(fname, x)
        y = imread(fname)

        assert_array_almost_equal((x * scaling).astype(np.int32), y)

    def test_imsave_roundtrip(self):
        dtype = np.uint8
        np.random.seed(0)
        for shape in [(10, 10), (10, 10, 3), (10, 10, 4)]:
            x = np.ones(shape, dtype=dtype) * np.random.rand(*shape)

            if np.issubdtype(dtype, np.floating):
                yield self.roundtrip, x, 255
            else:
                x = (x * 255).astype(dtype)
                yield self.roundtrip, x
