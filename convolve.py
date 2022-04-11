
from typing import Optional, List, Tuple
from argparse import ArgumentError

import numpy as np


class Kernel:
    def __init__(self, arr: np.ndarray):

        x, y = np.nonzero(arr)
        coords: List[Tuple[int, int]] = [(i, j) for i, j in zip(x, y)]
        values: List[int] = [arr[v] for v in coords]

        self.values = values
        self.coords = coords

        self.info = sorted([(int(val), x, y) for val, (x, y) in zip(values, coords)], key = lambda v: v[0])

        self.positive = [(x, y) for val, x, y in self.info if val == 1]
        self.negative = [(x, y) for val, x, y in self.info if val == -1]
        self.not_one = [(val, x, y) for val, x, y in self.info if abs(val) != 1]
        # на 0 не проверяю, так как это условие по определению выполняется

    @property
    def is_binary(self):
        return len(self.negative) == 0 and len(self.not_one) == 0

    @property
    def x(self):
        return np.array([t[1] for t in self.info], dtype = np.uint8)
    @property
    def y(self):
        return np.array([t[2] for t in self.info], dtype = np.uint8)

    @property
    def v_int(self):
        return np.array([t[0] for t in self.info], dtype = np.int8)
    @property
    def v_float(self):
        return np.array([t[0] for t in self.info], dtype = np.float32)




def _conv_numpy(image_padded: np.ndarray, ker: Kernel, out_image: np.ndarray):
    xs, ys = out_image.shape

    for x, y in ker.positive:
        out_image += image_padded[x:(xs + x), y:(ys + y)]

    if not ker.is_binary:  # есть ещё слагаемые, которые можно уже добавить; этот код самый долгий,
        # лучше не кидать во внутренние функции (наверное)
        for x, y in ker.negative:
            out_image -= image_padded[x:(xs + x), y:(ys + y)]

        for val, x, y in ker.not_one:
            out_image += val * image_padded[x:(xs + x), y:(ys + y)]



def apply_kernel_on_binary(image_bool: np.ndarray, kernel_int8: np.ndarray):

    assert np.issubdtype(image_bool.dtype, bool) and kernel_int8.dtype==np.int8, "wrong types of arrays"

    xs, ys = image_bool.shape
    xpad = int((kernel_int8.shape[0] - 1 ) /2)
    ypad = int((kernel_int8.shape[1] - 1 ) /2)
    ker = Kernel(kernel_int8[::-1, ::-1])

    image_padded = np.zeros(
        (xs + 2* xpad, ys + 2 * ypad),
        dtype=np.uint8
    )
    image_padded[xpad:(xs + xpad), ypad:(ys + ypad)] = image_bool

    result = np.zeros(
        (xs, ys),
        dtype=np.int8
    )

    _conv_numpy(image_padded, ker, result)

    return result


def apply_kernel_on_float(image_float: np.ndarray, kernel: np.ndarray):
    xs, ys = image_float.shape
    xpad = int((kernel.shape[0] - 1) / 2)
    ypad = int((kernel.shape[1] - 1) / 2)
    ker = Kernel(kernel[::-1, ::-1])

    image_padded = np.zeros(
        (xs + 2 * xpad, ys + 2 * ypad),
        dtype=np.float32
    )
    image_padded[xpad:(xs + xpad), ypad:(ys + ypad)] = image_float

    result = np.zeros(
        (xs, ys),
        dtype=np.float32
    )

    _conv_numpy(image_padded, ker, result)

    return result

