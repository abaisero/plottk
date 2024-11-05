import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
import matplotlib.pyplot as plt

from plottk.config import Config, DataConfig, FigConfig
from plottk.utils import remove_duplicates

sns.set_theme(style="darkgrid")


def plot(data: pd.DataFrame, config: Config, **kwargs) -> Axes:
    plot_kwargs = config.plot.kwargs.copy()

    if config.plot.name is not None:
        plot_config = config.plots[config.plot.name]
        plot_kwargs.update(plot_config.kwargs)

    plot_kwargs.update(kwargs)

    keys = config.data.keys.model_dump(exclude_none=True)
    if "estimator" in plot_kwargs:
        del keys["units"]
    else:
        plot_kwargs["estimator"] = None

    axes = sns.lineplot(data, **keys, **plot_kwargs)

    if config.fig is not None:
        process_fig(config.fig)

    return axes


def process_fig(config: FigConfig):
    if config.title is not None:
        plt.title(config.title)

    if config.xlim is not None:
        plt.xlim(config.xlim)

    if config.ylim is not None:
        plt.ylim(config.ylim)


def aggregate_x(data: pd.DataFrame, config: DataConfig) -> pd.DataFrame:
    if config.xagg is None:
        return data

    if config.xagg.xstep is None:
        assert config.xagg.xpoints is not None
        xmax = data[config.keys.x].max().item()
        xstep = xmax // config.xagg.xpoints
    else:
        xstep = config.xagg.xstep

    data = data.copy()
    data[config.keys.x] = data[config.keys.x].map(lambda x: x + xstep - x % xstep)
    groupkeys = [
        config.keys.hue,
        config.keys.style,
        config.keys.size,
        config.keys.units,
        config.keys.x,
    ]
    groupkeys = [key for key in groupkeys if key is not None]
    groupkeys = remove_duplicates(groupkeys)
    data_groupby = data.groupby(groupkeys)
    data_agg = data_groupby[config.keys.y].agg(config.xagg.agg)
    return data_agg.reset_index()
