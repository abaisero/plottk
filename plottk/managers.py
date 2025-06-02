import pathlib
from abc import ABCMeta, abstractmethod
from typing import Iterator, Type, cast

import pandas as pd
from slugify import slugify
from wandb.apis import PublicApi
from wandb.apis.public.runs import Run

from plottk.keys import Keys
from plottk.utils import Registry


class DataManager(metaclass=ABCMeta):
    def __init__(self, timeout: int | None = None):
        self.api = PublicApi(timeout=timeout)

    def runs(self, project: str, filters: dict) -> Iterator[Run]:
        yield from self.api.runs(project, filters=filters)

    @abstractmethod
    def make_run_label(self, run: Run) -> str:
        raise NotImplementedError

    def make_run_filename(self, run: Run, keys: Keys) -> str:
        label = self.make_run_label(run)
        slugified_key = slugify(keys.y)

        return f'{label}.{run.id}.{slugified_key}.pkl'

    def make_run_path(
        self, run: Run, keys: Keys, *, dir: str | pathlib.Path
    ) -> pathlib.Path:
        path = pathlib.Path(dir)
        return path / self.make_run_filename(run, keys)

    def load_run_data_local(
        self, run: Run, keys: Keys, *, dir: str | pathlib.Path
    ) -> pd.DataFrame:
        path = self.make_run_path(run, keys, dir=dir)
        data = pd.read_pickle(path)
        data = cast(pd.DataFrame, data)
        return data

    @abstractmethod
    def load_run_data_remote(self, run: Run, xkey: str, ykey: str) -> pd.DataFrame:
        raise NotImplementedError

    def load_run_data(
        self,
        run: Run,
        keys: Keys,
        *,
        dir: str | pathlib.Path,
        read_remote: bool = True,
        write_local: bool = True,
    ) -> pd.DataFrame:
        # read local
        try:
            return self.load_run_data_local(run, keys, dir=dir)
        except FileNotFoundError:
            if not read_remote:
                raise

        # read remote
        data = self.load_run_data_remote(run, keys.x, keys.y)

        if write_local:
            path = self.make_run_path(run, keys, dir=dir)
            path.parent.mkdir(parents=True, exist_ok=True)
            data.to_pickle(path)

        return data

    def load_data(
        self,
        project: str,
        filters: dict,
        keys: Keys,
        *,
        dir: str,
        read_remote: bool = True,
    ) -> Iterator[pd.DataFrame]:
        for run in self.runs(project, filters):
            try:
                data = self.load_run_data(
                    run,
                    keys,
                    dir=dir,
                    read_remote=read_remote,
                    write_local=run.state != 'running',
                )
                self.add_datafields(run, keys, data)
            except FileNotFoundError:
                continue

            yield data

    @abstractmethod
    def add_datafields(self, run: Run, keys: Keys, data: pd.DataFrame):
        raise NotImplementedError


datamanager_registry = Registry[Type[DataManager]]()


def make_datamanager(name: str, *, timeout: int | None = None) -> DataManager:
    datamanager_cls = datamanager_registry.get(name)
    return datamanager_cls(timeout)
