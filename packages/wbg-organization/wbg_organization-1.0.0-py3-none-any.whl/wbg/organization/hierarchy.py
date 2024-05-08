"""WBG unit hierarchy."""
import pandas as pd
import networkx as nx

from . import edc


def main() -> pd.DataFrame:
    df = edc.load_db(edc.Dataset.HIERARCHY)
    # _drop_closed(df)?
    _map = mapping(df)
    G = graph(_map)
    unique = _map.drop_duplicates(subset=['manager'])
    return expand(unique, G)


def _drop_closed(df: pd.DataFrame) -> pd.DataFrame:
    return df.loc[df['RETIRED_DATE'].isna()]


def mapping(df: pd.DataFrame) -> pd.DataFrame:
    """Return unit-subordinate mapping."""
    rename = {'MANAGING_UNIT_ID': 'manager', 'ORG_UNIT_ID': 'unit'}
    base = (
        df.rename(columns=rename)
        .filter(list(rename.values()))
        .dropna(subset=['manager'])
        .astype(int)
    )
    subordinate = pd.DataFrame(
        [(x, x) for x in base['unit'].unique()], columns=base.columns
    )
    concat = pd.concat([base, subordinate], ignore_index=True)

    return concat


def graph(mapping_: pd.DataFrame) -> nx.DiGraph:
    """Return directed graph of unit hierarchy."""
    G = nx.DiGraph()
    G.add_edges_from(mapping_.to_numpy())
    return G


def alpha_map(raw: pd.DataFrame) -> dict[int, str]:
    m = raw.filter(["ORG_UNIT_ID", "ALPHA_CODE"]).astype({"ORG_UNIT_ID": int})
    d_map = m.set_index("ORG_UNIT_ID").to_dict()
    return d_map['ALPHA_CODE']


def expand(mapping_: pd.DataFrame, g: nx.DiGraph) -> pd.DataFrame:

    col = 'unit'

    def _children(unit: int) -> set[int]:
        return nx.descendants(g, unit) | {unit}

    w_children = mapping_.assign(**{col: mapping_['manager'].apply(_children)})
    return w_children.explode(col)
