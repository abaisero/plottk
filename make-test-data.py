#!/usr/bin/env python

import numpy as np
import pandas as pd


def make_series(name: str, ndata: int) -> np.ndarray:
    if name == "linear":
        return np.linspace(-1, 1, ndata)

    if name == "sin":
        return np.sin(np.linspace(0, 4 * np.pi, ndata))

    raise ValueError(f"Invalid series name '{name}'")


def make_data(name: str, ndata: int, label: str, seed: int) -> pd.DataFrame:
    xs = np.arange(ndata)
    ys = make_series(name, ndata)

    # xnoise = np.random.normal(0, ndata / 100, ndata)
    ynoise = np.random.normal(0, 0.1, ndata)

    data = pd.DataFrame(
        {
            "x": xs,
            "y": ys + ynoise,
        }
    )
    data["label"] = label
    data["seed"] = seed

    return data


def main():
    N = 5_000

    data = []
    data += [make_data("linear", N, "Algo-A", seed) for seed in range(10)]
    data += [make_data("sin", N, "Algo-B", seed) for seed in range(5)]
    pd.concat(data).to_csv("test-data.csv", index=False)


if __name__ == "__main__":
    main()
