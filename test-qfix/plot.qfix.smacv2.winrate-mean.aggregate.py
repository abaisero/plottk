#!/bin/env python

import pathlib

import seaborn.objects as so
from matplotlib.ticker import EngFormatter
from shared import (
    hack_legend,
    make_color_values,
    make_data,
    make_label,
    make_plot,
    make_theme,
    preprocess_data,
    remove_legends,
)

from plottk.keys import Keys
from plottk.managers import make_datamanager
from plottk.utils import deepget, load_toml

name = 'smacv2'
datamanager = make_datamanager(name, timeout=60)
datadir = f'data/{name}'

flags = load_toml('flags.toml') | {
    'normalize': False,
    'interquantile': False,
}
dataconfig = load_toml('dataconfig.smacv2.winrate.toml')
runkeys = Keys(**dataconfig['keys']['run'])

project = dataconfig['project']
filters = dataconfig['filters']
data = make_data(datamanager, project, filters, runkeys, dir=datadir)
# TODO maybe relabel and change things here....?

keys = Keys(**dataconfig['keys']['data'])
data.rename(columns={runkeys.x: keys.x, runkeys.y: keys.y}, inplace=True)
data = preprocess_data(
    data,
    keys,
    relabel=dataconfig.get('relabel'),
    standardize_kwargs=deepget(dataconfig, 'standardize.kwargs'),
    normalize=flags['normalize'],
    interquantile=flags['interquantile'],
)

plotter = so.Plot(data, x=keys.x, y=keys.y, color=keys.group)

plotter = make_plot(plotter, data)

plotter = plotter.theme(make_theme())

plotter = plotter.scale(
    x=so.Continuous().label(EngFormatter()),
    y=so.Continuous().label(like='{x:1.0%}'),
)

plotter = plotter.scale(
    color=so.Nominal(
        make_color_values(),
        **load_toml('plotconfig.color-order.smacv2.toml'),
    )
)

limits = load_toml('plotconfig.xlimit.smacv2.toml')
limits |= load_toml('plotconfig.ylimit.smacv2.winrate.toml')
plotter = plotter.limit(**limits)

plotter = plotter.label(**make_label(keys, flags['normalize']))

# plotter = plotter.facet(**load_toml("plotconfig.facet.smacv2.toml"))
plotter = plotter.layout(size=(4, 1.85), engine='tight')
plotter = plotter.plot()

hack_legend(plotter._figure)

path = pathlib.Path('plots/qfix.smacv2.winrate-mean.aggregate.pdf')
path.parent.mkdir(parents=True, exist_ok=True)
plotter.save(path, bbox_inches='tight')

remove_legends(plotter._figure)

path = path.parent / f'{path.stem}.nolegend.pdf'
path.parent.mkdir(parents=True, exist_ok=True)
plotter.save(path, bbox_inches='tight')
