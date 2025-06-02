import pandas as pd

from plottk.keys import Keys
from plottk.managers import DataManager, Run, datamanager_registry


@datamanager_registry.register('smacv2')
class SMACV2_DataManager(DataManager):
    def load_run_data_remote(self, run: Run, xkey: str, ykey: str) -> pd.DataFrame:
        history = run.scan_history(keys=[xkey, ykey])
        return pd.DataFrame(history)

    def make_run_label(self, run: Run) -> str:
        map_name = run.config['env_args']['map_name']
        n_units = run.config['env_args']['capability_config']['n_units']
        n_enemies = run.config['env_args']['capability_config']['n_enemies']
        name = run.config['name']
        return f'smacv2.{map_name}-{n_units}vs{n_enemies}.{name}'

    def add_datafields(self, run: Run, keys: Keys, data: pd.DataFrame):
        data[keys.unit] = run.id
        data[keys.group] = run.config['name']

        map_name = run.config['env_args']['map_name']
        n_units = run.config['env_args']['capability_config']['n_units']
        n_enemies = run.config['env_args']['capability_config']['n_enemies']

        race = map_name.split('_')[1].capitalize()
        units = f'{n_units}vs{n_enemies}'
        task = f'{map_name}-{units}'

        data['map_name'] = map_name
        data['n_units'] = n_units
        data['n_enemies'] = n_enemies

        data['race'] = race
        data['units'] = units
        data[keys.task] = task


@datamanager_registry.register('overcooked')
class Overcooked_DataManager(DataManager):
    def load_run_data_remote(self, run: Run, xkey: str, ykey: str) -> pd.DataFrame:
        data = run.history(samples=5000, keys=[ykey], x_axis=xkey, pandas=True)
        assert isinstance(data, pd.DataFrame)
        return data

    def make_run_label(self, run: Run) -> str:
        layout = run.config['ENV_KWARGS']['layout']
        name = run.config['ALG_NAME']
        return f'overcooked-{layout}.{name}'

    def add_datafields(self, run: Run, keys: Keys, data: pd.DataFrame):
        data[keys.unit] = run.id
        data[keys.group] = run.config['ALG_NAME']

        layout = run.config['ENV_KWARGS']['layout']
        layout_map = {
            'cramped_room': 'Cramped Room',
            'asymm_advantages': 'Asymmetric Advantages',
            'coord_ring': 'Coordination Ring',
            'forced_coord': 'Forced Coordination',
            'counter_circuit': 'Counter Circuit',
        }
        data[keys.task] = layout_map[layout]


@datamanager_registry.register('role-of-state')
class RoleOfState_DataManager(DataManager):
    def load_run_data_remote(self, run: Run, xkey: str, ykey: str) -> pd.DataFrame:
        history = run.scan_history(keys=[xkey, ykey])
        return pd.DataFrame(history)

    def make_run_label(self, run: Run) -> str:
        env_label = run.config['env_label']
        algo_label = run.config['algo_label']
        return f'role-of-state.{env_label}.{algo_label}'

    def add_datafields(self, run: Run, keys: Keys, data: pd.DataFrame):
        data[keys.unit] = run.id
        data[keys.group] = run.config['algo_label']

        env_label = run.config['env_label']
        env_label_map = {
            'heavenhell-2': 'HeavenHell-2',
            'heavenhell-3': 'HeavenHell-3',
            'heavenhell-4': 'HeavenHell-4',
        }
        data[keys.task] = env_label_map[env_label]
