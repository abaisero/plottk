from typing import cast

import pandas as pd
import pytest

from plottk.config import load_config
from plottk.plotting import aggregate_x, augment_legend_counts, plot


@pytest.mark.parametrize(
    "filename",
    ["./test-config.toml"],
)
def test_load_config(filename: str):
    load_config(filename)


@pytest.mark.parametrize(
    "filename_config, filename_data, filename_output",
    [
        ("./test-config.toml", "./test-data.csv", "test-plots/plot.pdf"),
    ],
)
def test_plotting(filename_config: str, filename_data: str, filename_output: str):
    config = load_config(filename_config)
    data = pd.read_csv(filename_data)

    data = aggregate_x(data, config.data)
    axes = plot(data, config)
    key = cast(str, config.data.keys.hue)
    augment_legend_counts(axes, data, key, config.data)

    if (figure := axes.get_figure()) is not None:
        figure.savefig(filename_output, bbox_inches="tight")
