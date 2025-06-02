import pathlib
from typing import cast

import managers
import matplotlib.lines
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import tqdm
from matplotlib.figure import Figure

from plottk.keys import Keys
from plottk.managers import DataManager
from plottk.transformations import (
    filter_interquantile_data,
    normalize_data,
    standardize_data,
)
from plottk.utils import load_toml


def make_data(
    datamanager: DataManager,
    project: str,
    filters: dict,
    keys: Keys,
    *,
    dir: str,
):
    data = datamanager.load_data(project, filters, keys, dir=dir)
    data = tqdm.tqdm(data, desc='Loading data')
    data = pd.concat(data).reset_index(drop=True)
    return data


def preprocess_data(
    data: pd.DataFrame,
    keys: Keys,
    *,
    relabel: dict | None,
    standardize_kwargs: dict | None,
    normalize: bool,
    interquantile: bool,
) -> pd.DataFrame:
    if relabel is not None:
        data = data.replace({keys.group: relabel})

    if standardize_kwargs is not None:
        data = standardize_data(data, keys, **standardize_kwargs)

    if normalize:
        data = normalize_data(data, [keys.task], keys.y)

    if interquantile:
        data = filter_interquantile_data(data, keys)

    return data


def make_theme() -> dict:
    theme = {}
    theme |= sns.axes_style('whitegrid')
    theme['axes.spines.right'] = True
    theme |= sns.plotting_context('paper')
    return theme


def make_color_values() -> dict:
    config = load_toml('plotconfig.color.toml')
    palette = config['palette']
    indices = config['indices']

    palette = cast(list[str], sns.color_palette(palette, as_cmap=True))
    return {k: palette[i] for k, i in indices.items()}


def make_ylabel(ykey: str, normalized: bool) -> str:
    return f'{ykey} (Normalized)' if normalized else ykey


def make_label(keys: Keys, normalized: bool) -> dict:
    return {
        'x': keys.x,
        'y': make_ylabel(keys.y, normalized),
    }


def make_plot(plotter: so.Plot, data: pd.DataFrame) -> so.Plot:
    config = load_toml('plotconfig.statistics.toml')
    statistic = config['statistic']
    errorbar = config['errorbar']

    linewidth = 2

    plotter = plotter.add(
        so.Line(linewidth=linewidth),
        so.Agg(statistic),
    )

    # qfix_mask = data[keys.group].str.startswith('Q+FIX')
    # plotter = plotter.add(
    #     so.Line(linestyle='--', linewidth=linewidth),
    #     so.Agg(statistic),
    #     data=data.loc[~qfix_mask],
    #     legend=False,
    # )
    #
    # plotter = plotter.add(
    #     so.Line(linewidth=linewidth),
    #     so.Agg(statistic),
    #     data=data.loc[qfix_mask],
    # )

    plotter = plotter.add(
        so.Band(),
        so.Est(statistic, errorbar=errorbar),
    )

    return plotter


def remove_legends(fig: Figure):
    fig.legends.clear()


def hack_legend(fig: Figure):
    # NOTE: this would be nice, but no way to differentiate lines
    # for ax in fig.get_axes():
    #     for line in ax.get_lines():
    #         line.set_linestyle(":")

    for legend in fig.legends:
        for handle, text in zip(legend.legend_handles, legend.get_texts()):
            if handle is None:
                continue

            label = text.get_text()
            if label.startswith('Q+FIX'):
                continue

            if isinstance(handle, matplotlib.lines.Line2D):
                handle.set_linestyle(':')


def relabel_legend(fig: Figure, relabel: dict[str, str]):
    for legend in fig.legends:
        for text in legend.get_texts():
            label = text.get_text()

            try:
                new_label = relabel[label]
            except KeyError:
                pass
            else:
                text.set_text(new_label)
