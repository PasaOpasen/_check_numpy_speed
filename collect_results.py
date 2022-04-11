
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

    stat_dfs = []

    for path in paths:
        with open(path, 'r', encoding='utf8') as f:
            dct = json.load(f)

        name = Path(path).stem
        df = pd.DataFrame(dct).T

        df['version_'] = name

        stat_dfs.append(df)

    df = pd.concat(stat_dfs)

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


    rdf = pd.concat(
        [
            pd.DataFrame(d.drop('version_', 1).T.loc['mean', :]).T
            for d in stat_dfs
        ]
    )
    rdf.set_index(pd.Index([Path(path).stem for path in paths]), inplace=True)
    rdf['system_'] = Path(paths[0]).parent.stem

    return rdf




if __name__ == '__main__':

    dfs = []

    for folder in Path('./result').glob('*'):

        if not folder.is_dir():
            continue

        df = make_df(
            [str(folder.joinpath(js)) for js in ('pip.json', 'conda.json', 'conda_forge.json')],
            str(folder.joinpath('report.xlsx'))
        )

        dfs.append(df)


    df = pd.concat(dfs)
    df.to_excel('./result/info.xlsx')

    d2 = pd.DataFrame(
        {
            'system': df.system_.values,
            'source': list(df.index)
        }
    )
    df.drop('system_', 1, inplace=True)

    index = pd.MultiIndex.from_frame(d2)
    df.set_index(index, inplace=True)

    #"%.15g"
    df.to_excel('./result/info_system_source.xlsx')




