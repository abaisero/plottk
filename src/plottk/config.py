from __future__ import annotations

import tomllib
from typing import Optional, Self

from pydantic import BaseModel, Field, model_validator


def load_config(filename: str) -> Config:
    with open(filename, "rb") as f:
        config = tomllib.load(f)

    return Config(**config)


class Config(BaseModel):
    fig: Optional[FigConfig] = None
    data: DataConfig
    plot: PlotConfig
    plots: dict[str, PlotOptionConfig]


class FigConfig(BaseModel):
    title: Optional[str] = None
    xlim: Optional[tuple[float, float]] = None
    ylim: Optional[tuple[float, float]] = None


class DataConfig(BaseModel):
    keys: DataKeyConfig
    xagg: Optional[DataXAggConfig] = None


class DataKeyConfig(BaseModel):
    x: str
    y: str
    hue: Optional[str] = None
    size: Optional[str] = None
    style: Optional[str] = None
    units: str


class DataXAggConfig(BaseModel):
    agg: str
    xpoints: Optional[int] = None
    xstep: Optional[int] = None

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.xpoints is None and self.xstep is None:
            raise ValueError("One of `xpoints` or `xstep` is mandatory")
        return self


class PlotConfig(BaseModel):
    name: Optional[str] = None
    kwargs: dict = Field(default_factory=dict)


class PlotOptionConfig(BaseModel):
    kwargs: dict = Field(default_factory=dict)
