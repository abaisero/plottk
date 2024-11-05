from typer import Typer, Argument
import pandas as pd
from rich.console import Console
from plottk.config import load_config
from plottk.plotting import plot, aggregate_x
import matplotlib.pyplot as plt
from typing import cast
from typing_extensions import Annotated

app = Typer()
console = Console()


@app.command()
def csv(
    filename_data: Annotated[str, Argument(hidden=True, metavar="DATA.csv")],
    filename_config: Annotated[str, Argument(hidden=True, metavar="CONFIG.toml")],
):
    config = load_config(filename_config)
    data = pd.read_csv(filename_data)

    data = aggregate_x(data, config.data)
    plot(data, config)
    plt.show()


@app.command()
def pickle(
    filename_data: Annotated[str, Argument(hidden=True, metavar="DATA.csv")],
    filename_config: Annotated[str, Argument(hidden=True, metavar="CONFIG.toml")],
):
    config = load_config(filename_config)
    data = cast(pd.DataFrame, pd.read_pickle(filename_data))

    data = aggregate_x(data, config.data)
    plot(data, config)
    plt.show()


if __name__ == "__main__":
    app()
