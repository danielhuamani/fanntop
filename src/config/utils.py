import json
import os

def get_env(base_dir):
    """ Obtenemos las 'variables de entorno' desde un archivo json."""
    with open(os.path.join(base_dir, 'config/settings/settings.json')) as f:
        env = json.load(f)
        return env