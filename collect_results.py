
from typing import Sequence

from pathlib import Path

import json
import pandas as pd


# def make_df(path: str):
#
#     with open(path, 'r', encoding='utf8') as f:
#         dct = json.load(f)
#
#     df = pd.DataFrame(dct)
#
#     print()

def make_df(paths: Sequence[str], save_path: str):

    t = []

    for path in paths:
        with open(path, 'r', encoding='utf8') as f:
            dct = json.load(f)

        name = Path(path).stem
        df = pd.DataFrame(dct).T

        df['version_'] = name

        t.append(df)

    df = pd.concat(t)

    d2 = pd.DataFrame(
        {
            'version': df.version_.values,
            'old_index': list(df.index)
        }
    )
    df.drop('version_', 1, inplace=True)

    index = pd.MultiIndex.from_frame(d2)
    df.set_index(index, inplace=True)

    #"%.15g"
    df.to_excel(save_path)




if __name__ == '__main__':

    make_df(
        [
            './result/pip.json',
            './result/conda.json',
            './result/conda_forge.json',
        ],
        './result/report.xlsx'
    )



