
from typing import Sequence, Union, Callable, Dict

import os
import sys
import time
import json
import numpy as np

from convolve import apply_kernel_on_float, apply_kernel_on_binary



def summary(arr: Sequence[Union[int, float]]):

    if len(arr) == 0:
        return ''
    r = np.array(arr)

    return {
        'min': r.min(),
        '5%': np.quantile(r, 0.05),
        '25%': np.quantile(r, 0.25),
        'mean': r.mean(),
        'median': np.median(r),
        '75%': np.quantile(r, 0.75),
        '95%': np.quantile(r, 0.95),
        'max': r.max(),
        'count': r.size,
        'sum': r.sum()
    }


def get_func_summary(func: Callable, kwargs: Dict, count: int):

    vals = []

    #from tqdm import tqdm

    for _ in range(count + 1):
        t = time.time()
        func(**kwargs)
        vals.append(time.time() - t)

    return summary(vals[1:])


def test_sums(arr1: np.ndarray, arr2: np.ndarray):
    return arr1 + arr2 - arr1 - arr2 + arr1 * 2 + arr2 * 0.75 + (arr1-arr2)/4


def test_mult(arr: np.ndarray):
    return arr @ arr


def fill_test_data():

    np.random.seed(1)

    S = 100
    arr1 = np.random.random(S) * 4.5
    arr2 = -np.random.random(S)/2

    np.save('./data/arr1_small.npy', arr1)
    np.save('./data/arr2_small.npy', arr2)

    N, M = 1000, 1300
    arr1 = np.random.random((N, M)) * 4.5
    arr2 = -np.random.random((N, M))/2

    np.save('./data/arr1_big.npy', arr1)
    np.save('./data/arr2_big.npy', arr2)

    for S in (50, 200, 1000, 3000):
        arr = (np.random.random((S, S)) - 0.5)*4
        np.save(f'./data/arr_{S}.npy', arr)


def main(prefix: str = 'env_name'):

    load = lambda name: np.load(f"./data/{name}.npy")
    result = {}

    for name, func, kwargs, count in (
            ('sums small', test_sums, dict(arr1=load('arr1_small'), arr2=load('arr2_small')), 8000),
            ('sums big', test_sums, dict(arr1=load('arr1_big'), arr2=load('arr2_big')), 1000),
            ('mult 50', test_mult, dict(arr=load('arr_50')), 4000),
            ('mult 200', test_mult, dict(arr=load('arr_200')), 2000),
            ('mult 1000', test_mult, dict(arr=load('arr_1000')), 700),
            ('mult 3000', test_mult, dict(arr=load('arr_3000')), 50),
            ('convolve binary', apply_kernel_on_binary, dict(image_bool=load('bool_img'), kernel_int8=load('bool_kernel')), 400),
            ('convolve float', apply_kernel_on_float, dict(image_float=load('float_img'), kernel=load('float_kernel')), 150),
    ):
        print(f"running {name}")

        result[name] = get_func_summary(func, kwargs, count)


    with open(f'./result/{prefix}.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=1)

    os.system(
        f'cat /proc/version > {"./result/system.txt"}'
    )
    os.system(
        f'lscpu > {"./result/cpu.txt"}'
    )




if __name__ == '__main__':

    main(
        sys.argv[1]
    )






