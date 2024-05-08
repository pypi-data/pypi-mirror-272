"""Country Details"""
import functools as ft

# https://dataexplorer.worldbank.org/search/dataset/details?id=b478b877-faf7-ec11-bb3d-00224804dd77

from pathlib import Path
from typing import NoReturn
import pandas as pd


_SRC = 'https://dvresource.worldbank.org/docs/excel/COUNTRY.xlsx'


@ft.singledispatch
def load(obj: object) -> NoReturn:
    raise ValueError()


@load.register
def _str(url: str = _SRC) -> pd.DataFrame:
    return _load(url)


@load.register
def _path(file: Path) -> pd.DataFrame:
    return _load(file)


def _load(url: str | Path) -> pd.DataFrame:
    return pd.read_excel(url, header=4)


def clean(country_: pd.DataFrame) -> pd.DataFrame:
    clean = (
        country_.dropna(subset=['CNTRY_NME', 'WB_REGION_CDE'])
        .drop_duplicates()
        .rename(columns={'CNTRY_NME': 'country', 'WB_REGION_CDE': 'region'})
    )
    clean.loc[clean['country'].str.contains('United States|Canada'), 'region'] = 'NAR'

    return clean.assign(country=clean['country'].str.upper())
