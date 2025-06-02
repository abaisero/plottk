import pandas as pd

from plottk.keys import Keys
from plottk.managers import DataManager, Run, datamanager_registry


@datamanager_registry.register('heavenhell')
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
