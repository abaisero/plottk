from typing import cast

import numpy as np
import pandas as pd

from plottk.keys import Keys


def standardize_data(
    data: pd.DataFrame,
    keys: Keys,
    *,
    xmin: int | None = None,
    xmax: int | None = None,
    num: int = 100,
    window_size: int,
) -> pd.DataFrame:
    if xmin is None:
        xmin = cast(int, data[keys.x].min().item())

    if xmax is None:
        xmax = cast(int, data[keys.x].max().item())

    if window_size is None:
        window_size = (xmax - xmin) // num

    timesteps = np.linspace(xmin, xmax, num + 1).astype(int).tolist()[1:]
    timesteps = cast(list[int], timesteps)
    ranges = [(timestep - window_size + 1, timestep) for timestep in timesteps]

    by = [column for column in data.columns if column not in [keys.x, keys.y]]
    data = data.groupby(by).apply(
        lambda d: standardize_xs_windowed(d, timesteps, ranges, keys),
        include_groups=False,
    )

    data.index = data.index.droplevel(-1)
    data = data.reset_index()

    return data


def standardize_xs_windowed(
    run: pd.DataFrame,
    timesteps: list[int],
    ranges: list[tuple[int, int]],
    keys: Keys,
) -> pd.DataFrame:
    xs = run[keys.x]
    ys = run[keys.y]

    masks = [((start < xs) & (xs <= stop)) for start, stop in ranges]

    items = [
        {
            keys.x: timestep,
            keys.y: ys_window.mean(),
        }
        for timestep, mask in zip(timesteps, masks)
        if not (ys_window := ys.loc[mask]).empty
    ]

    return pd.DataFrame(items)
