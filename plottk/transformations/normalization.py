import pandas as pd


def normalize_data(
    data: pd.DataFrame,
    by: list[str],
    key: str,
    *,
    min: float | None = None,
    max: float | None = None,
) -> pd.DataFrame:
    groups = []
    for _, group in data.groupby(by):
        ys = group[key]
        ymin = ys.min() if min is None else min
        ymax = ys.max() if max is None else max
        group[key] = (ys - ymin) / (ymax - ymin)
        groups.append(group)

    data = pd.concat(groups).reset_index(drop=True)
    return data
