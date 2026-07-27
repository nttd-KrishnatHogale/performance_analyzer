from pathlib import Path
import yaml


class ConfigService:

    def __init__(self, config_path="config/config.yaml"):

        self.config_path = Path(config_path)

        self.config = self.load()

    def load(self):

        with open(self.config_path, "r") as f:

            return yaml.safe_load(f)

    def get(self, key, default=None):

        keys = key.split(".")

        value = self.config

        for k in keys:

            value = value.get(k)

            if value is None:

                return default

        return value