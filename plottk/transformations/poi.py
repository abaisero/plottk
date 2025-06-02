import numpy as np
import pandas as pd

from plottk.keys import Keys


def make_poi_data(data: pd.DataFrame, keys: Keys, baseline: str):
    groups = []
    for _, group in data.groupby([keys.task, keys.x]):
        baseline_mask = group[keys.group] == baseline
        baseline_data = group.loc[baseline_mask]

        group_ys = group[keys.y]
        for baseline_y in baseline_data[keys.y]:
            copy = group.copy()
            copy[keys.y] = 0.5 * np.sign(group_ys - baseline_y) + 0.5
            groups.append(copy)

    data = pd.concat(groups).reset_index(drop=True)
    return data
