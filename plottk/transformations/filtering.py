import pandas as pd

from plottk.keys import Keys


def filter_interquantile_data(data: pd.DataFrame, keys: Keys) -> pd.DataFrame:
    groups = []
    # NOTE: this is applying interqnautile filter to all tasks
    by = [keys.group, keys.x]
    for _, group in data.groupby(by):
        quantiles = group[keys.y].quantile([0.25, 0.75])
        iqr_mask = group[keys.y].between(*quantiles)
        groups.append(group.loc[iqr_mask])

    return pd.concat(groups).reset_index(drop=True)
