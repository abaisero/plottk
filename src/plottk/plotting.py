import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes

from plottk.config import Config, DataConfig, FigConfig, FormatterConfig
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


def get_formatter(config: FormatterConfig) -> matplotlib.ticker.Formatter:
    if config.name == "EngFormatter":
        return matplotlib.ticker.EngFormatter(*config.args, **config.kwargs)

    if config.name == "PercentFormatter":
        return matplotlib.ticker.PercentFormatter(*config.args, **config.kwargs)

    raise ValueError(f"Invalid formatter {config.name}")


def process_fig(config: FigConfig):
    axes = plt.gca()

    if config.title is not None:
        plt.title(config.title)

    if config.xlim is not None:
        plt.xlim(config.xlim)

    if config.ylim is not None:
        plt.ylim(config.ylim)

    if config.x_minor_formatter is not None:
        formatter = get_formatter(config.x_minor_formatter)
        axes.xaxis.set_minor_formatter(formatter)

    if config.x_major_formatter is not None:
        formatter = get_formatter(config.x_major_formatter)
        axes.xaxis.set_major_formatter(formatter)

    if config.y_minor_formatter is not None:
        formatter = get_formatter(config.y_minor_formatter)
        axes.yaxis.set_minor_formatter(formatter)

    if config.y_major_formatter is not None:
        formatter = get_formatter(config.y_major_formatter)
        axes.yaxis.set_major_formatter(formatter)


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


def get_counts(data: pd.DataFrame, key: str, config: DataConfig) -> dict[str, int]:
    return data.groupby(key)[config.keys.units].nunique().to_dict()


def augment_legend_counts(
    axes: Axes,
    data: pd.DataFrame,
    key: str,
    config: DataConfig,
):
    counts = get_counts(data, key, config)
    handles, labels = axes.get_legend_handles_labels()

    def make_label(label: str, counts: dict[str, int]) -> str:
        try:
            count = counts[label]
        except KeyError:
            return f"{label} (N/A)"
        else:
            return f"{label} ({count})"

    labels = [make_label(label, counts) for label in labels]
    axes.legend(handles=handles, labels=labels)
